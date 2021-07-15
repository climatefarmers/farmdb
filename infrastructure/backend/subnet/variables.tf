# Subnet variables

variable "region" {
  description = "Region of resources"
}

variable "subnet_name" {
    description = "Name of the subnet"
}

variable "subnet_cidr" {
  description = "Subnet range"
}

variable "vpc_name" {
  description = "The network we create the subnet in"
}