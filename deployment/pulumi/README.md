## Pulumi deployment 

1. Install and configure [pulumi](https://pulumi.io/quickstart/index.html)

2. Create new pulumi project in [Pulumi UI](https://app.pulumi.com/welcome) or with Pulumi CLI `pulumi new kubernetes-typescript` command. 

3. Connect to existing K8S cluster [or create one](https://pulumi.io/quickstart/kubernetes/index.html).

4. Create stack for your project e.g.: `dev` and configure it with your default [k8s context](https://pulumi.io/quickstart/kubernetes/setup.html):
```js
$ cd deployment/pulumi
$ pulumi stack init dev
$ export CURRENT_CONTEXT=$(kubectl config current-context)
$ pulumi config set --secret kubernetes:context $CURRENT_CONTEXT
$ pulumi config set --secret appImage your_container_image
$ pulumi config --show-secrets
```

5. To proceed with deployment run `pulumi up` and select `yes`:
```js
$ pulumi up
Previewing update (dev):

     Type                           Name                Plan       
 +   pulumi:pulumi:Stack            py-rest-api-v1-dev  create     
 +   ├─ kubernetes:apps:Deployment  pyapi               create     
 +   └─ kubernetes:core:Service     pyapi               create     
 
Resources:
    + 3 to create

Do you want to perform this update?
> yes
  no
  details
```

This will create POD deployment with given container `appImage` and `LoadBalancer` service with external IP:
```js
Updating (dev):

     Type                           Name                Status      
 +   pulumi:pulumi:Stack            py-rest-api-v1-dev  created     
 +   ├─ kubernetes:apps:Deployment  pyapi               created     
 +   └─ kubernetes:core:Service     pyapi               created     
 
Outputs:
    frontendIp: "35.204.xxx.xxx"

Resources:
    + 3 created

Duration: 1m11s

Permalink: https://app.pulumi.com/xxxxx/py-rest-api-v1/dev/updates/1
```

6. Test your rest api deployment with `curl` command:
```js
$ curl -sL $(pulumi stack output frontendIp):/api/status | jq
{
  "API_status": "OK"
}
```