variable "env" {
    description = "The environment to deploy"
    default = "dev"
}

variable "resource_group" {
    description = "A resource name prefix for grouping"
    default = "cfcommon"
}

variable "gcp_region" {
    description = "GCP region for deployments"
    default = "europe-west3"
}

variable "gcp_project_id" {
    description = "The GCS project to use"
}

# Postgres Variables
variable "postgres_db_name" {
    description = "Name for the postgres db"
    default = "pgfarmdb"
}

variable "postgres_version" {
    description = "Postgres version to use"
    default = "POSTGRES_11"
}

variable "postgres_host_tier" {
    description = "The tier of the machine to host postgres"
    default = "db-f1-micro"
}

variable "postgres_user" {
    description = "The username for the main pg account"
    default = "cfadmin"
}

# Kubernetes Variables

variable "kubernetes_cluster_name" {
    description = "Name for the kubernetes cluster"
    default = "atlas"
}

# Node Pool Variables

variable "node_count" {
    description = "The default number of nodes"
    default = 1
}

variable "node_tier" {
    description = "The tier of the machines in the node pool"
    default = "e2-medium"
}