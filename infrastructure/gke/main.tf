resource "google_service_account" "default" {
  account_id   = "service-account-id"
  display_name = "Service Account"
}

resource "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.region

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
  remove_default_node_pool = true
  initial_node_count       = 1

  # Use the VPC and subnetwork created
  network    = var.vpc_name
  subnetwork = var.subnet_name


  #addons_config {
  #  kubernetes_dashboard {
  #    disabled = false
  #  }
#
  #master_auth {
  #  username = "${var.gke_master_user}"
  #  password = "${var.gke_master_pass}"
  #}
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = var.gke_nodepool_name
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.gke_node_count

  node_config {
    preemptible  = true
    machine_type = var.gke_node_size

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}