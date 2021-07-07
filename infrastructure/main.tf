terraform {
  backend "s3" {
     bucket = "farmdb-tfstate"
     key = "farmdb.tfstate"
     region = "eu-west3"
     endpoint = "https://storage.googleapis.com"
     skip_credentials_validation = true
  }
}


provider "google" {
  project     = "idyllic-silicon-318213"
  region      = "eu-west3"
}


resource "google_sql_database_instance" "farmdb-postgres" {
  name             = "farmdb"
  database_version = "POSTGRES_11"
  region           = "eu-west3"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
  }
}