'''                                                                                                                           Tests for dockerized rest_api 
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

class TestApiStatus(object):
    '''
    test API status 
    '''

    def test_apiStatus(self):
        ''' test API status '''

        url = tstcfg.apiUrl + '/status'
        r = requests.get(url)

        assert r.json()['API_status'] == 'OK'
