'''                                                                                                                           Tests for dockerized rest_simple python REST api tests with py.test
'''

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

tstcfg.apiUrl = 'http://localhost:5002/api'


##############################
# Tests section starts here  #
##############################

## GET API STATUS
class TestApiStatus(object):
    '''
    test API status 
    '''

    def test_apiGetStatus(self):
        ''' test API GET status '''

        url = tstcfg.apiUrl + '/status'
        r = requests.get(url)

        assert r.json()['API_status'] == 'OK'

## GET      
class TestApiGet(object):
    '''
    test API GET responses
    '''

    def test_apiGetEmployees(self):
        ''' test API GET employees '''

        url = tstcfg.apiUrl + '/v1/employees'
        r = requests.get(url)

        assert type(r.json()) is dict

    def test_apiGetEmployeeId(self):
        ''' test API GET employee ID with ID=1'''

        url = tstcfg.apiUrl + '/v1/employees/1'
        r = requests.get(url)

        assert type(r.json()) is dict

# ## POST
# class TestApiPost(object):
#     '''
#     test API POST responses
#     '''

#     def test_apiPostEmployeesId(self):
#         ''' test API POST with new employee creation '''

#         url = tstcfg.apiUrl + '/v1/employees/new'

#         with open('app/payload.json', 'r') as f:
#             payload = json.load(f)
#             r = requests.post(url, json=payload)

#             assert r.status_code == 201

        
