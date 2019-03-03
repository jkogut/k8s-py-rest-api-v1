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
            matchLabels {
                app = "pyapi"
                tier = "web"
            }
        }

        template {
            metadata {
                labels {
                    app = "pyapi"
                    tier = "web"
                }
            }
            spec {
                containers {
                    name = "pyapi"
                    image = "${var.image}"

                    resources {
                        requests {
                            cpu = "100m"
                            memory = "100Mi"
                        }
                    }

                    ports {
                        containerPort = 5002
                    }
                }
            }
        }
    }
}