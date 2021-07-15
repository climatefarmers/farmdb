# GCP variables
variable "region" {
  description = "Region of resources"
}

# Cloud SQL variables

variable "availability_type" {
  description = "Availability type for HA"
}

variable "sql_name" {
  description = "Name of database"
}

variable "sql_instance_size" {
  description = "Size of Cloud SQL instances"
}

variable "sql_version" {
  description = "Version to use"
}

variable "sql_disk_type" {
  description = "Cloud SQL instance disk type"
}

variable "sql_disk_size" {
  description = "Storage size in GB"
}

variable "sql_require_ssl" {
  description = "Enforce SSL connections"
}

variable "sql_connect_retry_interval" {
  description = "The number of seconds between connect retries."
}

variable "sql_deletion_protection" {
  description = "Set to false to allow terraform to destroy the database"
}

variable "sql_master_zone" {
  description = "Zone of the Cloud SQL master (a, b, ...)"
}

variable "sql_replica_zone" {
  description = "Zone of the Cloud SQL replica (a, b, ...)"
}

variable "sql_user" {
  description = "Username of the host to access the database"
}

variable "sql_pass" {
  description = "Password of the host to access the database"
  sensitive = true
}

variable "vpc_name" {
  description = "The private network to place this database in"
}