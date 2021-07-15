resource "google_sql_database_instance" "main" {
  name             = var.sql_name
  database_version = var.sql_version
  region           = var.region
  deletion_protection = var.sql_deletion_protection

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = var.sql_instance_size
    availability_type = var.availability_type
    disk_size = var.sql_disk_size
    disk_type = var.sql_disk_type

    ip_configuration {
      private_network = var.vpc_name
      require_ssl  = var.sql_require_ssl
      ipv4_enabled = true
    }

    backup_configuration {
      # binary_log_enabled = true
      enabled            = true
      start_time         = "00:00"
    }

  }
}

resource "google_sql_user" "user" {
  depends_on = [
    google_sql_database_instance.main
  ]
  instance = google_sql_database_instance.main.name
  #type     = "CLOUD_IAM_USER"
  name     = var.sql_user
  password = var.sql_pass
}
