### K8S deployment
**[Docker](#docker)**<br>
**[GKE](#gke)**<br>
**[Terraform](#terraform)**<br>
**[Pulumi](#pulumi)**<br>

Docker
------

**(!)** As a prerequisite you need to build docker image and publish it to your favorite
container repository. Example for GCR repository with **project ID=[YOUR_PROJECT_ID]**: 

```js
$ git clone git@github.com:jkogut/simple-python-rest-api-v1.git
$ sudo docker build --tag simple_python_rest_api:1.0.0 .
$ sudo docker tag simple_python_rest_api:1.0.0 gcr.io/[YOUR_PROJECT_ID]/simple_python_rest_api:1.0.0
$ gcloud auth configure-docker
$ sudo docker push gcr.io/[YOUR_PROJECT_ID]/simple_python_rest_api:1.0.0
```

GKE
---

Create K8S cluster using **GKE**:
```js
$ gcloud container clusters create py-rest-api-v1 --num-nodes=3
```
