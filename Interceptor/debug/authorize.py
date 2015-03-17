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

from HalfkeyHandler import HalfkeyHandler

global half
half = HalfkeyHandler()

global Eaddr,passwd
Eaddr = "magiclamp1010@gmail.com"
passwd = "202154215471"


def Authorize():
  global half
  email = "facetumn@gmail.com"
  UnamePass = half.GetHalfkey(email)
  if UnamePass != None:
    Pass = UnamePass[1]
    print "time to start proxy: " + str(time.time())
    proc = subprocess.Popen(["python", "proxy.py", Pass], stdout = subprocess.PIPE)
    proc.wait()
    print proc.stdout.readlines()

Authorize()
