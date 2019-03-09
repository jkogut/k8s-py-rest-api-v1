### PULUMI TROUBLESHOOTING


```js
$ pulumi up --yes
Previewing update (dev):

     Type                           Name                Plan       
     pulumi:pulumi:Stack            py-rest-api-v1-dev             
 +   ├─ kubernetes:apps:Deployment  pyapi               create     
 +   ├─ kubernetes:core:Service     pyapi               create     
 -   ├─ kubernetes:core:Service     nginx               delete     
 -   └─ kubernetes:apps:Deployment  nginx               delete     
 
Resources:
    + 2 to create
    - 2 to delete
    2 changes. 1 unchanged

Updating (dev):

     Type                           Name                Status                  Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev                          
 +   └─ kubernetes:apps:Deployment  pyapi               **creating failed**     1 error
 
System Messages
  ^C received; cancelling. If you would like to terminate immediately, press ^C again.
  Note that terminating immediately may lead to orphaned resources and other inconsistencies.
  
 
Diagnostics:
  kubernetes:apps:Deployment (pyapi):
    error: Plan apply failed: 4 errors occurred:
    
    * Resource operation was cancelled for 'pyapi-ge0pwsdq'
    * [MinimumReplicasUnavailable] Deployment does not have minimum availability.
    * Minimum number of live Pods was not attained
    * 1 Pods failed to run because: [ImagePullBackOff] Back-off pulling image "gcr.io/gke_xxxxxx-231316/simple_python_rest_api:1.0.0"
 
Resources:
    1 unchanged

Duration: 4m51s

Permalink: https://app.pulumi.com/xxxxx/py-rest-api-v1/dev/updates/3
error: update failed
```

```js
$ kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
nginx-q4oeshs2-54d84976f7-xgqh2   1/1     Running            0          23m
pyapi-ge0pwsdq-7dd6675777-29pln   0/1     ImagePullBackOff   0          15m
```

- then provide a proper image:

```js
$ pulumi up --yes
Previewing update (dev):

     Type                           Name                Plan       Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev             
 ~   ├─ kubernetes:apps:Deployment  pyapi               update     [diff: ~spec]
 +   ├─ kubernetes:core:Service     pyapi               create     
 -   ├─ kubernetes:core:Service     nginx               delete     
 -   └─ kubernetes:apps:Deployment  nginx               delete     
 
Resources:
    + 1 to create
    ~ 1 to update
    - 2 to delete
    3 changes. 1 unchanged

Updating (dev):

     Type                           Name                Status                  Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev                          
 ~   └─ kubernetes:apps:Deployment  pyapi               **updating failed**     [diff: ~spec]; 1 error
 
Diagnostics:
  kubernetes:apps:Deployment (pyapi):
    error: Plan apply failed: 4 errors occurred:
    
    * Timeout occurred for 'pyapi-ge0pwsdq'
    * [MinimumReplicasUnavailable] Deployment does not have minimum availability.
    * Minimum number of live Pods was not attained
    * 1 Pods failed to schedule because: [Unschedulable] 0/1 nodes are available: 1 Insufficient cpu.
 
Resources:
    1 unchanged

Duration: 5m4s

Permalink: https://app.pulumi.com/jkogut/py-rest-api-v1/dev/updates/4
error: update failed
```

- so now I have 3 pods :D and no resources left ....

```js
$ kubectl get pods
NAME                              READY   STATUS             RESTARTS   AGE
nginx-q4oeshs2-54d84976f7-xgqh2   1/1     Running            0          41m
pyapi-ge0pwsdq-7c79cfcbc9-sx9x7   0/1     Pending            0          8m
pyapi-ge0pwsdq-7dd6675777-29pln   0/1     ImagePullBackOff   0          33m
```

So I am stuck, and have to:
- convince somehow `pulumi` to remove pod with ERRORS first: `pyapi-ge0pwsdq-7dd6675777-29pln` since it has an `ImagePullBackOff` errors we DO NOT NEED THIS CONTAINER ANYWAY

- update our `index.ts` config with some resource limits:
```js
resources:
          requests:
            cpu: 100m
            memory: 100Mi
```

- so update your code with: `resources: { requests: { cpu: "100m", memory: "100Mi" } }`
unfortunatelly, no effect


```js
Updating (dev):

     Type                           Name                Status                  Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev                          
 ~   └─ kubernetes:apps:Deployment  pyapi               **updating failed**     [diff: ~spec]; 1 error
 
Diagnostics:
  kubernetes:apps:Deployment (pyapi):
    error: Plan apply failed: 3 errors occurred:
    
    * Timeout occurred for 'pyapi-ge0pwsdq'
    * Minimum number of Pods to consider the application live was not attained
    * 1 Pods failed to schedule because: [Unschedulable] 0/1 nodes are available: 1 Insufficient cpu.
 
Resources:
    1 unchanged

Duration: 5m4s
```

**(!)** but ..... kubectl shows ...

```js
$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
nginx-q4oeshs2-54d84976f7-xgqh2   1/1     Running   0          1h
pyapi-ge0pwsdq-6b75878bb8-vzgdv   0/1     Pending   0          10m
pyapi-ge0pwsdq-7c79cfcbc9-sx9x7   1/1     Running   0          37m
```

lets see what is going on with our resources: `$ kubectl describe node ...`
```js
Non-terminated Pods:         (11 in total)
  Namespace                  Name                                                        CPU Requests  CPU Limits  Memory Requests  Memory Limits   AGE
  ---------                  ----                                                        ------------  ----------  ---------------  -------------   ---
  default                    nginx-q4oeshs2-54d84976f7-xgqh2                             100m (10%)    0 (0%)      0 (0%)           0 (0%)          74m
  default                    pyapi-ge0pwsdq-7c79cfcbc9-sx9x7                             100m (10%)    0 (0%)      0 (0%)           0 (0%)          42m
  kube-system                event-exporter-v0.2.3-85644fcdf-bxc6r                       0 (0%)        0 (0%)      0 (0%)           0 (0%)          3h32m
  kube-system                fluentd-gcp-scaler-8b674f786-wjhwt                          0 (0%)        0 (0%)      0 (0%)           0 (0%)          3h32m
  kube-system                fluentd-gcp-v3.2.0-gcpvl                                    100m (10%)    1 (106%)    200Mi (7%)       500Mi (18%)     3h31m
  kube-system                heapster-v1.6.0-beta.1-688675bb64-pddmj                     138m (14%)    138m (14%)  301456Ki (11%)   301456Ki (11%)  3h31m
  kube-system                kube-dns-6b98c9c9bf-4c8kg                                   260m (27%)    0 (0%)      110Mi (4%)       170Mi (6%)      3h32m
  kube-system                kube-dns-autoscaler-67c97c87fb-rtwlf                        20m (2%)      0 (0%)      10Mi (0%)        0 (0%)          3h32m
  kube-system                kube-proxy-gke-py-rest-api-v1-default-pool-99d83354-p0dj    100m (10%)    0 (0%)      0 (0%)           0 (0%)          3h31m
  kube-system                l7-default-backend-7ff48cffd7-vdlhw                         10m (1%)      10m (1%)    20Mi (0%)        20Mi (0%)       3h32m
  kube-system                metrics-server-v0.2.1-fd596d746-5m5bz                       53m (5%)      148m (15%)  154Mi (5%)       404Mi (15%)     3h31m
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests        Limits
  --------           --------        ------
  cpu                881m (93%)      1296m (137%)
  memory             807312Ki (29%)  1421712Ki (52%)
  ephemeral-storage  0 (0%)          0 (0%)
  ```

  **Lets requests even less CPU for our pyapi service.**
  `100m --> 50m` 

```js
$ pulumi up --yes
Previewing update (dev):

     Type                           Name                Plan       Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev             
 ~   ├─ kubernetes:apps:Deployment  pyapi               update     [diff: ~spec]
 +   ├─ kubernetes:core:Service     pyapi               create     
 -   ├─ kubernetes:core:Service     nginx               delete     
 -   └─ kubernetes:apps:Deployment  nginx               delete     
 
Resources:
    + 1 to create
    ~ 1 to update
    - 2 to delete
    3 changes. 1 unchanged

Updating (dev):

     Type                           Name                Status      Info
     pulumi:pulumi:Stack            py-rest-api-v1-dev              
 ~   ├─ kubernetes:apps:Deployment  pyapi               updated     [diff: ~spec]
 +   ├─ kubernetes:core:Service     pyapi               created     
 -   ├─ kubernetes:core:Service     nginx               deleted     
 -   └─ kubernetes:apps:Deployment  nginx               deleted     
 
Outputs:
  ~ frontendIp: "35.204.226.113" => "35.204.242.122"

Resources:
    + 1 created
    ~ 1 updated
    - 2 deleted
    3 changes. 1 unchanged

Duration: 52s

Permalink: https://app.pulumi.com/jkogut/py-rest-api-v1/dev/updates/7
```

and how about resoucres ???

```js
Non-terminated Pods:         (10 in total)
  Namespace                  Name                                                        CPU Requests  CPU Limits  Memory Requests  Memory Limits   AGE
  ---------                  ----                                                        ------------  ----------  ---------------  -------------   ---
  default                    pyapi-ge0pwsdq-7d77fcc78-tkdkb                              50m (5%)      0 (0%)      100Mi (3%)       0 (0%)          2m57s
  kube-system                event-exporter-v0.2.3-85644fcdf-bxc6r                       0 (0%)        0 (0%)      0 (0%)           0 (0%)          3h40m
  kube-system                fluentd-gcp-scaler-8b674f786-wjhwt                          0 (0%)        0 (0%)      0 (0%)           0 (0%)          3h40m
  kube-system                fluentd-gcp-v3.2.0-gcpvl                                    100m (10%)    1 (106%)    200Mi (7%)       500Mi (18%)     3h39m
  kube-system                heapster-v1.6.0-beta.1-688675bb64-pddmj                     138m (14%)    138m (14%)  301456Ki (11%)   301456Ki (11%)  3h39m
  kube-system                kube-dns-6b98c9c9bf-4c8kg                                   260m (27%)    0 (0%)      110Mi (4%)       170Mi (6%)      3h40m
  kube-system                kube-dns-autoscaler-67c97c87fb-rtwlf                        20m (2%)      0 (0%)      10Mi (0%)        0 (0%)          3h40m
  kube-system                kube-proxy-gke-py-rest-api-v1-default-pool-99d83354-p0dj    100m (10%)    0 (0%)      0 (0%)           0 (0%)          3h39m
  kube-system                l7-default-backend-7ff48cffd7-vdlhw                         10m (1%)      10m (1%)    20Mi (0%)        20Mi (0%)       3h40m
  kube-system                metrics-server-v0.2.1-fd596d746-5m5bz                       53m (5%)      148m (15%)  154Mi (5%)       404Mi (15%)     3h39m
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests        Limits
  --------           --------        ------
  cpu                731m (77%)      1296m (137%)
  memory             909712Ki (33%)  1421712Ki (52%)
  ephemeral-storage  0 (0%)          0 (0%)
  ```

  yes, as we can see load of `cpu 731m (77%)` fell to 77% from `(93%)` and `pulumi` was able not to crash (good!!!)
  now, lets add `containerPort`  