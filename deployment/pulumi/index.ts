import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

// lets take image from pulumi config
let config = new pulumi.Config();
let appImage = config.get("appImage");

// nginx container, replicated 1 time.
const appName = "pyapi";
const appLabels = { app: appName };
const nginx = new k8s.apps.v1beta1.Deployment(appName, {
    spec: {
        selector: { matchLabels: appLabels },
        replicas: 1,
        template: {
            metadata: { labels: appLabels },
            spec: { containers: [
                        { 
                            name: appName, 
                            image: appImage                            
                        }] 
                    }
        }
    }
});

// Allocate an IP to the nginx Deployment.
const frontend = new k8s.core.v1.Service(appName, {
    metadata: { labels: nginx.spec.apply(spec => spec.template.metadata.labels) },
    spec: {
        type: "LoadBalancer",
        ports: [{ port: 80, targetPort: 80, protocol: "TCP" }],
        selector: appLabels
    }
});

// When "done", this will print the public IP.
export let frontendIp = frontend.status.apply(status => status.loadBalancer.ingress[0].ip);
