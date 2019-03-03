resource "kubernetes_service" "pyapiweb" {
    metadata {
        name = "pyapiweb"
        labels {
            app = "pyapi"
        }
    }
    spec {
        selector {
            app = "pyapi"
            tier = "web"
        }
        
        type = "LoadBalancer"
        
        ports {
            port = 80
            targetPort = 5002
        }
    }
}