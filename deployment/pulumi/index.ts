import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

// lets take image from pulumi config
let config = new pulumi.Config();
let appImage = config.require("appImage");

// testapp container, replicated 1 time.
const appName = "pyapi";
const appLabels = { app: appName };
const testapp = new k8s.apps.v1beta1.Deployment(appName, {
    spec: {
        selector: { matchLabels: appLabels },
        replicas: 1,
        template: {
            metadata: { labels: appLabels },
            spec: { containers: [
                        { 
                            name: appName, 
                            image: appImage,
                            resources: { requests: { cpu: "50m", memory: "100Mi" } },
                            ports: [{ containerPort: 5002 }]
                        }]
                    }
        }
    }
});

// allocate an IP to the testapp Deployment.
const frontend = new k8s.core.v1.Service(appName, {
    metadata: { labels: testapp.spec.apply(spec => spec.template.metadata.labels) },
    spec: {
        type: "LoadBalancer",
        ports: [{ port: 80, targetPort: 5002, protocol: "TCP" }],
        selector: appLabels
    }
});

// when "done", this will print the public IP.
export let frontendIp = frontend.status.apply(status => status.loadBalancer.ingress[0].ip);
