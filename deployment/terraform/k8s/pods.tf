resource "kubernetes_replication_controller" "pyapi" {
    metadata {
        name = "pyapi"
    
        labels {
            app = "pyapi"
        }
    }
    spec {
        replicas = 1

        selector {
            app = "pyapi"
            tier = "web"
        }

        template {
            metadata {
                labels {
                    app = "pyapi"
                    tier = "web"
                }
            }
            spec {
                container {
                    name = "pyapi"
                    image = "${var.image}"

                    resources {
                        requests {
                            cpu = "100m"
                            memory = "100Mi"
                        }
                    }

                    port {
                        container_port = 5002
                    }
                }
            }
        }
    }
}