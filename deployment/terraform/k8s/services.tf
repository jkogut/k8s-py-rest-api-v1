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
        
        port {
            port = 80
            target_port = 5002
        }
    }
}