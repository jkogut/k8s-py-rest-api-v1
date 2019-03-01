### K8S deployment
**[Docker](#docker)**<br>
**[GKE](#gke)**<br>
**[Terraform](#terraform)**<br>
**[Pulumi](#pulumi)**<br>

Docker
------

**(!)** As a prerequisite you need to build docker image and publish it to your favorite
container repository. Example for [GCR](https://cloud.google.com/container-registry/) repository: 

- build the image:
```js
$ git clone git@github.com:jkogut/simple-python-rest-api-v1.git
$ sudo docker build --tag simple_python_rest_api:1.0.0 .
```
- configure docker to access GCR, retag and push the image:
```js
$ gcloud auth configure-docker
$ export PROJECT_ID="$(gcloud config get-value project -q)"
$ sudo docker tag simple_python_rest_api:1.0.0 gcr.io/${PROJECT_ID}/simple_python_rest_api:1.0.0
$ sudo docker push gcr.io/${PROJECT_ID}/simple_python_rest_api:1.0.0
```

GKE
---

Create K8S cluster using **GKE**:
```js

$ gcloud container clusters create py-rest-api-v1 --num-nodes=3
$ kubectl run simple-python-rest-api --image=gcr.io/${PROJECT_ID}/simple_python_rest_api:1.0.0 --port 8080
```
