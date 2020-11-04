#This file contains functions for authorizing yourself for the RM-cloud

#TODO: What more does this module do?
#TODO: Implement logging of requests and responses
#TODO: Implement testing?


import requests
import uuid

class Client:
    """Class for authorizing and requesting towards the cloud

    Once the class has authorized the user to the cloud, it will store the bearer token that is needed
    for communicating with the cloud.
    """
    def __init__(self, rm_code, token=False, device_id=False, device_desc='desktop-Windows'):
        self.token = token
        self.rm_code = rm_code
        self.device_id = device_id
        self.device_desc = device_desc

        if not self.device_id:
            self.generate_device_id()

        if not self.token:
            self.generate_bearer_token()
        else:
            self.refresh_token()

    def generate_bearer_token(self):
        """Register this application as new device and generates a new Bearer Authentication token."""
        payload = {'code': self.rm_code,
                   'deviceDesc': self.device_desc,
                   'deviceID': self.device_id}

        response = requests.post('https://my.remarkable.com/token/json/2/device/new', data=payload)
        if not response.ok:
            print('The request failed')
        else:
            new_token = str(response.content)
            print('Newly generated token: {}'.format(new_token)) #TODO: Remove
            self.token = new_token
        return new_token


    def generate_device_id(self):
        """ Generates an UUID4 code which can be used as device identification towards the rm."""
        self.device_id = uuid.uuid4()
        print('New UUID4: {}'.format(self.device_id))

    def refresh_token(self):
        """Refreshes the token (if it exists)"""
        if self.token is not None:
            header = {'Authorization': 'Bearer ' + self.token}
            response = requests.post('https://my.remarkable.com/token/json/2/device/new', headers=header)
            print('Refresh response: {}'.format(response))

    def request(self, verb, url, data={}, **kwargs):
        """Send HTTP-requests to the cloud.

        Keyword arguments:
            verb[String] -- type of HTTP-request (GET, PUT, POST, ...) #TODO: What else
            url[String] -- request url
            data[String] - request data

        Returns:
             response[?] -- request response
        """
        pass


if __name__ == '__main__':
    client = Client('YOUR RM CODE HERE')

