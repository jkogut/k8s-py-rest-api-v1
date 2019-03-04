### Variables
variable "project" {}
variable "region" {}
variable "zone" {}
variable "username" {}
variable "password" {}
variable "clustername" {}
variable "nodecount" {}
variable "image" {}

### Modules
module "gke" {
  source   = "./gke"
  project  = "${var.project}"
  region   = "${var.region}"
  zone     = "${var.zone}"
  clustername = "${var.clustername}"
  nodecount = "${var.nodecount}"
  username = "${var.username}"
  password = "${var.password}"
}

module "k8s" {
  source   = "./k8s"
  host     = "${module.gke.host}"
  image    = "${var.image}"
  username = "${var.username}"
  password = "${var.password}"

  client_certificate     = "${module.gke.client_certificate}"
  client_key             = "${module.gke.client_key}"
  cluster_ca_certificate = "${module.gke.cluster_ca_certificate}"
}