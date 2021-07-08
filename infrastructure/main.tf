terraform {
  backend "gcs" {
     bucket = "farmdb-tfstate"
     prefix = "terraform/farmdb"
  }
}


provider "google" {
  project     = "idyllic-silicon-318213"
  region      = "europe-west3"
}


resource "google_sql_database_instance" "farmdb-postgres" {
  name             = "farmdb"
  database_version = "POSTGRES_11"
  region           = "europe-west3"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
  }
}