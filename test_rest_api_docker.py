"""
Tests for dockerized rest_simple python REST api tests with py.test
"""

__author__     = "Jan Kogut"
__copyright__  = "Jan Kogut"
__license__    = "MIT"
__version__    = "0.0.1"
__maintainer__ = "Jan Kogut"
__status__     = "Beta"


import requests
import json


##############################
# Config section starts here #
##############################

class TestConfig(object):
    pass

tstcfg = TestConfig()

tstcfg.apiUrl = 'http://0.0.0.0:5002/api'


##############################
# Tests section starts here  #
##############################

## GET API STATUS
class TestApiStatus(object):
    """ test API status """

    def test_apiGetStatus(self):
        """ test API GET status """

        url = tstcfg.apiUrl + '/status'
        r = requests.get(url)
        assert r.json()['API_status'] == 'OK'

        
## GET      
class TestApiGet(object):
    """ test API GET responses """

    def test_apiGetEmployees(self):
        """ test API GET employees """

        url = tstcfg.apiUrl + '/v1/employees'
        r = requests.get(url)
        assert type(r.json()) is dict


    def test_apiGetEmployeeId(self):
        """ test API GET employee ID with ID=1 """

        url = tstcfg.apiUrl + '/v1/employees/1'
        r = requests.get(url)
        assert type(r.json()) is dict

        
## POST
class TestApiPost(object):
    """ test API POST responses """

    def test_apiPostFakeEmployeesId(self):
        """ test API POST with new employee creation """

        url = tstcfg.apiUrl + '/v1/employees/new'
        with open('app/fake_payload.json', 'r') as f:
            payload = json.load(f)
            r = requests.post(url, json=payload)
            assert r.status_code == 400


    def test_apiPostEmployeesId(self):
        """ test API POST with new employee creation """

        url = tstcfg.apiUrl + '/v1/employees/new'
        with open('app/payload.json', 'r') as f:
            payload = json.load(f)
            r = requests.post(url, json=payload)
            assert r.status_code == 201

            
## DELETE
class TestApiDelete(object):
    """ test API DELETE responses """

    def test_apiDeleteNonExistentEmployee(self):
        """ test API DELETE with non existent employee's Id """

        urlGet  = tstcfg.apiUrl + '/v1/employees'
        rGet    = requests.get(urlGet) # GET all employees
        empNum  = len(rGet.json()) # count them
        empNum  = empNum + 100 # be sure Id is non-existent
        urlDel  = tstcfg.apiUrl + '/v1/employees/delete/' + str(empNum)
        rDelete = requests.delete(urlDel) # DELETE non-existent 
        assert rDelete.status_code == 400 # EXPECT BAD REQUEST

        
    def test_apiDeleteExistentEmployee(self):
        """ test API DELETE with employee's Id """

        with open('app/payload.json', 'r') as f:
            payload     = json.load(f)
            empLastName = payload['LastName'] 

        urlGet  = tstcfg.apiUrl + '/v1/employees'
        rGet    = requests.get(urlGet) # GET all empoyees

        empDict = rGet.json()['employees'] # use a dict to represent employees

        for key in empDict: # get employee's Id by his LastName
            if empDict[key] == empLastName:
                empId   = key
                urlDel  = tstcfg.apiUrl + '/v1/employees/delete/' + empId
                rDelete = requests.delete(urlDel) # DELETE empoyee
                assert rDelete.status_code == 200 # OK
