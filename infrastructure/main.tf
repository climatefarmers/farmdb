terraform {
  backend "gcs" {
     bucket = "farmdb-tfstate"
     prefix = "terraform/farmdb"
  }
}


provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region
}


resource "random_password" "postgres_password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

###################################################################################################
# Networking
###################################################################################################

resource "google_compute_network" "custom" {
  name                    = "${var.resource_group}-vpc-${var.env}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "custom" {
  name          = "${var.resource_group}-subnet-${var.env}"
  ip_cidr_range = "10.5.0.0/20"
  region        = var.gcp_region
  network       = google_compute_network.custom.id
  secondary_ip_range {
    range_name    = "services-ip-range"
    ip_cidr_range = "10.4.0.0/19"
  }

  secondary_ip_range {
    range_name    = "pods-ip-range"
    ip_cidr_range = "10.0.0.0/14"
  }
}

###################################################################################################
# Cloud SQL and DB
###################################################################################################

resource "google_sql_database_instance" "primary" {
  name             = "${var.resource_group}-${var.postgres_db_name}-${var.env}"
  database_version = var.postgres_version
  region           = var.gcp_region

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = var.postgres_host_tier

    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.custom.self_link
    }
  }
}

resource "google_sql_database" "farmdb" {
  name     = "farmdb"
  instance = google_sql_database_instance.primary.name
}


resource "google_sql_user" "db_user" {
  name     = var.postgres_user
  instance = google_sql_database_instance.primary.name
  password = random_password.postgres_password.result
}

###################################################################################################
# GKE and nodepool
###################################################################################################

resource "google_service_account" "gke" {
  account_id   = "${var.resource_group}-gke-serviceaccount"
}

resource "google_container_cluster" "primary" {
  name     = "${var.resource_group}-${var.kubernetes_cluster_name}-${var.env}"
  location = "${var.gcp_region}-a" #Zonal cluster instead of regional with replicas in 3 zones 

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.custom.id
  subnetwork = google_compute_subnetwork.custom.id

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods-ip-range"
    services_secondary_range_name = "services-ip-range"
  }

  #private_cluster_config {
  #  enable_private_nodes = true
  #  master_ipv4_cidr_block = "127.16.0.0/28"
  #}

  workload_identity_config {
    identity_namespace = "${var.gcp_project_id}.svc.id.goog"
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${var.resource_group}-${var.kubernetes_cluster_name}-nodepool-${var.env}"
  location   = "${var.gcp_region}-a" #Zonal cluster instead of regional with replicas in 3 zones 
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = var.node_tier

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.gke.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}


###################################################################################################
# K8s setup
###################################################################################################


data "google_client_config" "provider" {}

provider "kubernetes" {
  host  = "https://${google_container_cluster.primary.endpoint}"
  token = data.google_client_config.provider.access_token
  cluster_ca_certificate = base64decode(
    google_container_cluster.primary.master_auth[0].cluster_ca_certificate,
  )
}


resource "kubernetes_namespace" "farmdb" {
  metadata {
    annotations = {
      name = "farmdb-namespace"
    }

    name = "farmdb"
  }
}

resource "kubernetes_secret" "postgres-secret" {
  metadata {
    name = "postgres-secret"
    namespace = kubernetes_namespace.farmdb.metadata.0.name
  }

  data = {
    username = var.postgres_user
    password = random_password.postgres_password.result
    database = google_sql_database.farmdb.name
  }

  type = "kubernetes.io/basic-auth"
}


###################################################################################################
# Cloud SQL proxy GSA-KSA binding through workload identity
###################################################################################################

module "my-app-workload-identity" {
  source     = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  name       = "${var.resource_group}-sql-proxy-${var.env}"
  namespace  = kubernetes_namespace.farmdb.metadata.0.name
  project_id = var.gcp_project_id
  roles = ["roles/cloudsql.admin"]
}


###################################################################################################
# Static IP
###################################################################################################

resource "google_compute_global_address" "default" {
  name = "${var.resource_group}-ip-${var.env}"
}

###################################################################################################
# ArgoCD
###################################################################################################

module "argo_cd" {
  source = "runoncloud/argocd/kubernetes"

  namespace       = "argocd"
  argo_cd_version = "2.0.3"
}

###################################################################################################
# Static file bucket
###################################################################################################
resource "google_storage_bucket" "static" {
  name          = "${var.resource_group}-static-${var.env}"
  location      = "EU"
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_service_account" "static" {
  account_id   = "${var.resource_group}-static-gsa-${var.env}"
}

resource "google_service_account_key" "static" {
  service_account_id = google_service_account.static.name
}

resource "kubernetes_secret" "static" {
  metadata {
    name = "static-gsa-credentials"
    namespace = kubernetes_namespace.farmdb.metadata.0.name
  }
  data = {
    "credentials.json" = base64decode(google_service_account_key.static.private_key)
  }
}

data "google_iam_policy" "static" {
  binding {
    role = "roles/storage.admin"
    members = [
      "serviceAccount:${google_service_account.static.email}",
    ]
  }
}

resource "google_storage_bucket_iam_policy" "static" {
  bucket = google_storage_bucket.static.name
  policy_data = data.google_iam_policy.static.policy_data
}