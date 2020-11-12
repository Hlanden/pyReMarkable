#This file contains functions for authorizing yourself for the RM-cloud

#The only thing you need is to define the code for your remarkable.
#
#The module will store your code and your device-id as a keyring in the native keyring-manager, the first time you
# launch it (only tested on Windows).
#
#Once it has created or fetched the information from the keyring, it will generate a Bearer Token used for communcation.


#TODO: What more does this module do?
#TODO: Implement logging of requests and responses
#TODO: Implement testing?


import requests
import uuid
import keyring
import browser_cookie3

class Client:
    """Class for authorizing and requesting towards the cloud-server

    Once the class has authorized the user to the cloud, it will store the bearer token that is needed
    for communicating with the cloud.
    """
    def __init__(self, rm_code='', token=''):
        """Intitializing the client.

         It will first try to fetch the rm-code and device-id from a keyring called "pyRm"(see the native credidential
         manager). If it cannot find the keyring it will create a new one with the same name, give that you have
         provided the rm_code. If not it will raise an exception.

        Once it has set the rm_code and device_id it will request the cloud for a Bearer Token which is needed for
        sending requests to the cloud service

        Keyword arguments:
            rm_code[String] -- The code from your remarkable, generated at https://my.remarkable.com/connect/remarkable
            token[String] -- the Bearer Token for the cloud service (TODO: May be removed)
            device_id[String] - UUID4 identification for current device
        """
        self.token = token
        self.device_id = ''
        self.device_desc = 'desktop-windows'
        self.rm_code = rm_code
        print('Rm code: {}'.format(rm_code))
        if not self.get_token_and_id_from_keyring() or rm_code:
            self.rm_code = rm_code
            if not self.device_id:
                self.generate_device_id()
            self.generate_bearer_token()
            self.set_new_key_ring()
        else:
            print('Successfully got RM-token and device-ID from keyring')

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
            self.token = credentials.password
            return True

    def set_new_key_ring(self):
        """Create new keyring with device id and rm-code

        :return: True if success else False
        """
        if self.device_id and self.token:
            keyring.set_password('pyRm', self.device_id, self.token)
            return True
        else:
            return False

    def update_key_ring(self):
        keyring.delete_password('pyRm', self.device_id)
        keyring.set_password('pyRm', self.device_id, self.token)

    def generate_bearer_token(self):
        """Register this application as new device and generates a new Bearer Authentication token."""
        payload = {'code': self.rm_code,
                   'deviceDesc': self.device_desc,
                   'deviceID': str(self.device_id)}

        response = requests.post('https://my.remarkable.com/token/json/2/device/new', json=payload, headers={})
        if not response.ok:
            raise Exception('Request failed, could not connect')
        else:
            self.token = response.content.decode('utf-8')


    def generate_device_id(self):
        """ Generates an UUID4 code which can be used as device identification towards the rm."""
        self.device_id = str(uuid.uuid4())
        print('New UUID4: {}'.format(self.device_id))

    def refresh_token(self):
        """Refreshes the token (if it exists)

        NOTE: This is only used to check connection, because you don't need to refresh tokens for remarkable (yet)"""
        if self.token is not None:
            header = {'Authorization': 'Bearer {}'.format(self.token)}
            response = requests.post('https://my.remarkable.com/token/json/2/user/new', headers=header)
            if response.ok:
                print('Connected to remarkable!')
            else:
                Exception('Failed to refresh token...')


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
    Client = Client(input('Enter RM code: '))

