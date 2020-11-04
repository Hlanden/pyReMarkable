#This file contains functions for authorizing yourself for the RM-cloud

#TODO: What more does this module do?
#TODO: Implement logging of requests and responses
#TODO: Implement testing?


import requests
import uuid
import keyring

class Client:
    """Class for authorizing and requesting towards the cloud-server

    Once the class has authorized the user to the cloud, it will store the bearer token that is needed
    for communicating with the cloud.
    """
    def __init__(self, rm_code= '', token='', device_id='', device_desc='desktop-Windows'):
        self.token = token
        self.rm_code = rm_code
        self.device_id = device_id
        self.device_desc = device_desc

        if not rm_code:
            if not self.get_token_and_id_from_keyring():
                print('Please enter a valid RM code')
            else:
                print('Successfully got RM-code and device-ID from keyring')
        else:
            if not self.get_token_and_id_from_keyring():
                self.generate_device_id()
                self.set_new_key_ring()
            else:
                print('Successfully got RM-code and device-ID from keyring')

        if not self.token:
            self.generate_bearer_token()
        else:
            self.refresh_token()

    def get_token_and_id_from_keyring(self):
        """Get device id and rm-code from keyring

        :return: True if success else False
        """
        credentials = keyring.get_credential('pyRm', None)
        if credentials is None:
            print('No credentials set for this computer')
            return False
        else:
            self.device_id = credentials.username
            self.rm_code = credentials.password
            return True

    def set_new_key_ring(self):
        """Create new keyring with device id and rm-code

        :return: True if success else False
        """
        if self.device_id and self.rm_code:
            keyring.set_password('pyRm', self.device_id, self.rm_code)
            print('New keyring created')
            return True
        else:
            return False

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
        self.device_id = str(uuid.uuid4())
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



