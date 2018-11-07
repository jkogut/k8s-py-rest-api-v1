# simple-python-rest-api-v1
Simple python REST API with docker and travis-ci 


[![Build Status](https://travis-ci.org/jkogut/simple-python-rest-api-v1.svg?branch=master)](https://travis-ci.org/jkogut/simple-python-rest-api-v1)

Install
-------

clone the repo first and then build the docker image and run it

```
docker build --tag simple_python_rest_api .
docker run -p 127.0.0.1:5002:5002 -d simple_python_rest_api
```

test it with *py.test*

`py.test -v -l test_rest_api_docker.py`
