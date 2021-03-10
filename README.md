# pyReMarkable 
**NOTE: This is a work in progress, and is still missing a lot of functionality**

Python API for interfacing with Remarkable-cloud application.

The library contains the following python modules:
## client.py
Contains a client class for authorizing towards the reMarkable-cloud service. It also contains functions to send HTTP-requests to the cloud server. The first time you connect to the reMarkable, you will need to use a generated rm_code which you can require from https://my.remarkable.com/connect/remarkable. The device-id for this python application and the bearer-token will be saved in the keyring-manager in the OS for later usage. This means you only need to enter the rm-code the first time you use the application.

## List of TODOs:
  - Connect to RM [DONE]
  - Upload to RM
  - Download from RM [DONE]
  - Convert from .rm to .pdf. This is the current bottleneck. I have not found any engines that can do this flawlessly...
