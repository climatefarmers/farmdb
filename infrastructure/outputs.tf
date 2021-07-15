# network VPC output
output "vpc_name" {
  value       = "${module.vpc.vpc_name}"
  description = "The unique name of the network"
}

# subnet cidr ip range
output "ip_cidr_range" {
  value       = "${module.subnet.ip_cidr_range}"
  description = "Export created CICDR range"
}

# Cloud SQL postgresql outputs
output "master_instance_sql_ipv4" {
  value       = "${module.cloudsql.master_instance_sql_ipv4}"
  description = "The IPv4 address assigned for master"
}

# GKE outputs
output "endpoint" {
  value       = "${module.gke.endpoint}"
  description = "Endpoint for accessing the master node"
}
output "sql_pass" {
  value = "${random_password.sql_password.result}"
  description = "Password of the host to access the database"
  sensitive = true
}

output "gke_master_pass" {
  value = "${random_password.k8s_password.result}"
  description = "Password to authenticate with the k8s master"
  sensitive = true
}