variable "vpc_name" {
    description = "The network we create the firewall for"
}

variable "int_name" {
    description = "The name for the internal traffic firewall"
}

variable "ext_name" {
    description = "The name for the external traffic firewall"
}

variable "ip_cidr_range" {
    description = "The IP range from the subnet"
}