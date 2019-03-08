# k8s-py-rest-api-v1
Proof of concept for deployment to k8s of simple python REST API  


[![Build Status](https://travis-ci.org/jkogut/k8s-py-rest-api-v1.svg?branch=master)](https://travis-ci.org/jkogut/k8s-py-rest-api-v1)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)


### Table of Contents
**[Install locally](#install)**<br>
**[Deploy to K8S](deployment/DEPLOYMENT.md)**<br>
**[Run tests](#test)**<br>
**[Debug](#debug)**<br>


Install
-------

To install locally clone the repo first, then build the docker image and run it:

```js
$ git clone git@github.com:jkogut/simple-python-rest-api-v1.git
$ docker build --tag simple_python_rest_api .
$ docker run -p 127.0.0.1:5002:5002 -d simple_python_rest_api
```

Run tests with *pytest* to check if **API** works:

```js
$ py.test -v -l test_rest_api_docker.py
```

Test
----

Test available endpoints with **curl**:

 * [GET] API status *http://0.0.0.0:5002/api/status*
 * [GET] Employees  *http://0.0.0.0:5002/api/v1/employees*
 * [GET] Employee full data   *http://0.0.0.0:5002/api/v1/employees/EmployeeId*
 * [POST] Create new employee *http://0.0.0.0:5002/api/v1/employees/new*
 * [DELETE] Delete employee *http://0.0.0.0:5002/api/v1/employees/delete/EmployeeId*
 
Example usage: 
```js
$ curl http://0.0.0.0:5002/api/status |jq
$ curl http://0.0.0.0:5002/api/v1/employees |jq
$ curl http://0.0.0.0:5002/api/v1/employees/1 |jq
$ curl -H "Content-Type: application/json" -X POST -d@payload.json http://0.0.0.0:5002/api/v1/employees/new |jq
$ curl -X DELETE http://0.0.0.0:5002/api/v1/employees/delete/9 |jq
```

Debug
-----

Clone the repo:

```js
$ git clone git@github.com:jkogut/simple-python-rest-api-v1.git
```

Use `virtualenv` and install dependencies with `pip`:
```js
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r app/requirements.txt
```

Run flask rest application in `debug mode`:
```js
$ cd app;
$ python rest_server.py
```
