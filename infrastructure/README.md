# Terraform description of main infrastructure

### Sets up the following cloud resources:
- VPC
- Subnet
- Cloud SQL Instance
- Kubernetes

### Additionally configures:
- KSA - GSA pairing for cloud sql proxy
- K8s secret with database credentials
- ArgoCD


### Manual steps necessary: 
- Connect to DB using psql as postgres superuser and run (ssh into a cluster node or setup temporary VM in same VPC)
- CREATE EXTENSION postgis;
- CREATE EXTENSION postgis_topology;

