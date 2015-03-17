# provide email related functionality.

# user send email, whose subject should be: "request", body include:
# "yourskypename".

import time
import email, imaplib, os, random, sys
import smtplib
import subprocess



from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders



sys.path.append(os.getcwd() + "/CredentialHandler/")
sys.path.append(os.getcwd() + "/twitter_api/")

from HalfkeyHandler import HalfkeyHandler
from CredentialHandler import CredentialHandler
from DecentralAuthorize import DecentAuthMachine
from TwitterHandler import TwitterHandler
import UtilEmail 

global half
half = HalfkeyHandler()

global credential
credential = CredentialHandler()

global Eaddr,passwd
Eaddr = "magiclamp1000@gmail.com"
passwd = "202154215471"






def Authorize():
  global half, Eaddr
  global credential 

  email = "facetumn@gmail.com"
  UnamePass = half.GetHalfkey(email) 
  if UnamePass != None:
    au = DecentAuthMachine(UnamePass[0], UnamePass[1])
    access_token = au.Authorize()

    # store credential if it exists
    if access_token != None:
      credential.UpdateCredential(email, access_token[0], access_token[1])
      # notify user
      print "success!"
    else:
      print "fail"
    
  
Authorize()

