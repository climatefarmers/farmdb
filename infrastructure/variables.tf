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

# Network variables
variable "subnet_cidr" {
  default = {
    prod = "10.10.0.0/24"
    dev  = "10.240.0.0/24"
  }

  description = "Subnet range"
}

# Cloud SQL variables

variable "sql_db_name" {
    description = "Name for the db"
    default = "farmdb"
}

variable "sql_version" {
    description = "Version to use"
    default = "POSTGRES_11"
}

variable "availability_type" {
  default = {
    prod = "REGIONAL"
    dev  = "ZONAL"
  }

  description = "Availability type for HA"
}

variable "sql_instance_size" {
  default     = "db-f1-micro"
  description = "Size of Cloud SQL instances"
}

variable "sql_disk_type" {
  default     = "PD_SSD"
  description = "Cloud SQL instance disk type"
}

variable "sql_disk_size" {
  default     = "10"
  description = "Storage size in GB"
}

variable "sql_require_ssl" {
  default     = "false"
  description = "Enforce SSL connections"
}

variable "sql_master_zone" {
  default     = "a"
  description = "Zone of the Cloud SQL master (a, b, ...)"
}

variable "sql_replica_zone" {
  default     = "b"
  description = "Zone of the Cloud SQL replica (a, b, ...)"
}

variable "sql_connect_retry_interval" {
  default     = 60
  description = "The number of seconds between connect retries."
}

variable "sql_user" {
  default     = "cfadmin"
  description = "Username of the host to access the database"
}

variable "sql_deletion_protection" {
    description = "Set to false to allow terraform to destroy the database"
    default = true
}



# Kubernetes Variables

variable "gke_cluster_name" {
    description = "Name for the kubernetes cluster"
    default = "k8s"
}

# Node Pool Variables

variable "gke_node_count" {
    description = "The default number of nodes"
    default = {
        prod = 2
        dev  = 1
    }

}

variable "gke_node_size" {
    description = "The size of the machines in the node pool"
    default = {
        prod = "e2-small"
        dev = "e2-micro"
    }
}

variable "gke_master_user" {
  default     = "cfadmin"
  description = "Username to authenticate with the k8s master"
}
