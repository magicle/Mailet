# use user's password to obtain the session cookie
# arg[0]:     username
# return      success or not

import sys
import os
import binascii

os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'

sys.path.append(os.getcwd() + "/CredentialHandler/")

from CookieManager import CookieManager
from TwitterConnector import TwitterConnector

from HalfkeyHandler import HalfkeyHandler





def main():

  # obtain passcode
  emailaddr = sys.argv[1]
  half = HalfkeyHandler()
  res = half.GetHalfkey(emailaddr)
  username = res[0]
  passcode = res[1]



  con = TwitterConnector(1)
  #con.SetCookie(out)
  con.InitConn('cookie', {'username':username, 'passcode':passcode})
  print("InitConn finished")
  
  con.Start()
  print("Start finished")
  
  con.PickThenReconstruct()
  print("PickThenReconstruct finished") 
  
  res = con.ReceiveResponse()
  print("ReceiveResponse finished:", res)
 
  if res != None: 
    cook = CookieManager('cookie/')
    cook.Write(username, res)
    sys.exit(1)
  else:
    sys.exit(0)

if __name__ == "__main__":
  main()


