# pyReMarkable
Python library for interfacing with Remarkable-cloud appllication.

The library contains the following python modules:
## client.py
Contains a client class for authorizing towards the reMarkable-cloud service. It also contains functions to send HTTP-requests to the cloud server. The first time you connect to the reMarkable, you will need to use a generated rm_code which you can require from https://my.remarkable.com/connect/remarkable. The device-id for this python application and the code/token (figure out which) will be saved in the keyring-manager in the OS for later usage.

List of TODOs:
  - Connect to RM
  - Upload to RM
  - Download from RM
