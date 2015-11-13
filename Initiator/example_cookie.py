import sys
import os
import binascii

os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'

sys.path.append(os.getcwd() + "/CredentialHandler/")

from CookieManager import CookieManager
from TwitterConnector import TwitterConnector


con = TwitterConnector(1)
#con.SetCookie(out)
con.InitConn('cookie', {})
print("InitConn finished")

con.Start()
print("Start finished")

con.PickThenReconstruct()
print("PickThenReconstruct finished") 

con.ReceiveResponse()
print("ReceiveResponse finished")






