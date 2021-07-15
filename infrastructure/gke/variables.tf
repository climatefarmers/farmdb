# GKE variables

variable "region" {
  description = "Region of resources"
}

variable "gke_node_count" {
  description = "Number of nodes in each GKE cluster zone"
}

variable "vpc_name" {
  description = "vpc name"
}
variable "subnet_name" {
  description = "subnet name"
}

variable "gke_cluster_name" {
  description = "Name of the gke cluster"
}

variable "gke_nodepool_name" {
  description = "The name of the gke node pool"
}

variable "gke_master_user" {
  description = "Username to authenticate with the k8s master"
}

variable "gke_master_pass" {
  description = "The password to authenticate with k8s master"
}

variable "gke_node_size" {
  description = "Machine type of GKE nodes"
}

