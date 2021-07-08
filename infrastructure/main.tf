terraform {
  backend "gcs" {
     bucket = "farmdb-tfstate"
     prefix = "terraform/farmdb"
  }
}


provider "google" {
  project     = var.gcs_project_id
  region      = var.gcp_region
}


resource "google_sql_database_instance" "farmdb-postgres" {
  name             = "${var.resource_group}-${var.postgres_db_name}-${var.env}"
  database_version = var.postgres_version
  region           = var.gcp_region

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = var.postgres_host_tier
  }
}


resource "google_service_account" "default" {
  account_id   = "service-account-id"
  display_name = "Service Account"
}

resource "google_container_cluster" "primary" {
  name     = "${var.resource_group}-${var.kubernetes_cluster_name}-${var.env}"
  location = var.gcp_region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${var.resource_group}-${var.kubernetes_cluster_name}-nodepool-${var.env}"
  location   = var.gcp_region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  node_config {
    preemptible  = true
    machine_type = var.node_tier

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}