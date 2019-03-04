### GKE vars
variable "project" {}
variable "region" {}
variable "zone" {}
variable "username" {
    default = "admin"
}
variable "password" {}

variable "clustername" {}
variable "nodecount" {}
