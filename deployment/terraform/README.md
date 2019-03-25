Terraform
---------

1. Configure terraform with GKE:

```js
$ export TF_PROJ=$(gcloud config get-value project)
$ export TF_CREDS=~/.secrets/gcloud/terraform.json

$ gcloud iam service-accounts create terraform \
--display-name "Terraform admin account"

$ gcloud iam service-accounts keys create ${TF_CREDS} \
--iam-account terraform@${TF_PROJ}.iam.gserviceaccount.com
 
$ gcloud projects add-iam-policy-binding ${TF_PROJ} \
--member serviceAccount:terraform@${TF_PROJ}.iam.gserviceaccount.com \
 --role='roles/container.admin'
 ```

2. Organize terraform files:

```js
.
├── gke
│   ├── cluster.tf
│   └── vars.tf
├── k8s
│   ├── k8s.tf
│   ├── pods.tf
│   ├── services.tf
│   └── vars.tf
├── main.tf
└── terraform.tfvars
```

3. Run deployment with terraform:

```js
$ terraform init
$ terraform plan
$ terraform apply 
```