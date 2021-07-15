terraform {
  required_providers {
      google = {
      source  = "hashicorp/google"
      version = "3.74.0"
      }
  }

  backend "gcs" {
     bucket = "farmdb-tfstate"
     prefix = "terraform/farmdb"
  }
}

provider "google" {
  project     = "${var.gcp_project_id}"
  region      = "${var.gcp_region}"
}

resource "random_password" "sql_password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

resource "random_password" "k8s_password" {
  length           = 16
  special          = true
  override_special = "_%@"
}

module "vpc" {
  source   = "./backend/vpc"
  vpc_name = "${var.resource_group}-vpc-${var.env}"
}

module "subnet" {
  source      = "./backend/subnet"
  subnet_name = "${var.resource_group}-subnet-${var.env}"
  region      = "${var.gcp_region}"
  vpc_name    = "${module.vpc.vpc_name}"
  subnet_cidr = "${var.subnet_cidr[terraform.workspace]}"
}

module "firewall" {
  source        = "./backend/firewall"
  int_name      = "${var.resource_group}-firewall-int-${var.env}"
  ext_name      = "${var.resource_group}-firewall-ext-${var.env}"
  vpc_name      = "${module.vpc.vpc_name}"
  ip_cidr_range = "${module.subnet.ip_cidr_range}"

  #  subnet_cidr                 = "${var.subnet_cidr}"
}

module "cloudsql" {
  source                     = "./cloudsql"
  region                     = "${var.gcp_region}"
  availability_type          = "${var.availability_type[terraform.workspace]}"
  sql_name                   = "${var.resource_group}-sql-${var.env}"
  sql_version                = "${var.sql_version}"
  sql_instance_size          = "${var.sql_instance_size}"
  sql_disk_type              = "${var.sql_disk_type}"
  sql_disk_size              = "${var.sql_disk_size}"
  sql_require_ssl            = "${var.sql_require_ssl}"
  sql_master_zone            = "${var.sql_master_zone}"
  sql_connect_retry_interval = "${var.sql_connect_retry_interval}"
  sql_replica_zone           = "${var.sql_replica_zone}"
  sql_user                   = "${var.sql_user}"
  sql_pass                   = random_password.sql_password.result
  sql_deletion_protection    = "${var.sql_deletion_protection}"
  vpc_name                   = "${module.vpc.vpc_name}"
}

module "gke" {
  source                = "./gke"
  region                = "${var.gcp_region}"
  gke_cluster_name      = "${var.resource_group}-k8s-${var.env}"
  gke_nodepool_name     = "${var.resource_group}-nodepool-${var.env}"
  gke_node_count        = "${var.gke_node_count[terraform.workspace]}"
  gke_node_size         = "${var.gke_node_size[terraform.workspace]}"
  gke_master_user       = "${var.gke_master_user}"
  gke_master_pass       = random_password.k8s_password.result
  vpc_name              = "${module.vpc.vpc_name}"
  subnet_name           = "${module.subnet.subnet_name}"
}