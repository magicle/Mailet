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
from CookieManager import CookieManager

global half
half = HalfkeyHandler()

global Eaddr,passwd
Eaddr = "magiclamp1010@gmail.com"
passwd = "202154215471"

def Branch(mail):
    if mail["Subject"] == "password":
      PassWord(mail)
      return 1
    elif mail["Subject"] == "posttweet" or "retweet" in mail['Subject']: 
      PostRetweet(mail)
      return 1
    else:
      return 0
      


# PostRetweet:    post or retweet 
def PostRetweet(mail):
  # get username
  emailaddr = mail['from']
  global half
  username = half.GetHalfkey(emailaddr)[0]
  
  # get half cookie
  cook = CookieManager('./cookie/')
  cookie = cook.Read(username)

  # start proxy.py
  FNULL = open(os.devnull, "w")
  proc = subprocess.Popen(['python3.4', 'proxy.py', cookie, username], stdout=FNULL, stderr=FNULL)
  proc.wait()
  print("[PostRetweet:returncode]\t\t", proc.returncode)
  


# stores the half credential
def PassWord(mail):
  global half, Eaddr
  emailaddr = mail["from"]
  UnamePass = BodyOneLine(mail)
  
  account = UnamePass.split()[0]
  password = UnamePass.split()[1]

  half.UpdateHalfkey(emailaddr, account, password)
  MailBack(emailaddr, "Success for " + Eaddr, "Partial Credential Received")
  

  # start proxy to split the credential
  FNULL = open(os.devnull, 'w')
  proc = subprocess.Popen(['python3.4', 'proxy.py', password, account, emailaddr])
  proc.wait()


def BodyOneLine (msg):  
  maintype = msg.get_content_maintype()
  if maintype == 'multipart':
    for index, part in enumerate(msg.walk()):
      if index == 1:
        result = part.get_payload().split("\n")[0]

  elif maintype == 'text':
    result =  msg.get_payload().split("\n",1)[0]
  return result.strip("\n\r")






def MailBack(Who, Msg, Subject):
    global Eaddr, passwd
    fromaddr = Eaddr
    toaddrs  = Who
    username = Eaddr.split("@")[0]
    password = passwd

    headers = ["from: "+ fromaddr, "subject: "+ Subject]
    headers = "\r\n".join(headers)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, headers + "\r\n\r\n" + Msg)
    server.quit()



def init():
    if not os.path.exists("HalfCredential"):
        f = open("HalfCredential", "w")
        f.write("\n")
        f.close
    return 1

init()
while 1:
    time.sleep(1)
    detach_dir = '.' # directory where to save attachments (default: current)
    user = Eaddr.split("@")[0]
    pwd = passwd

# connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes


    resp, items = m.search(None, "UNSEEN") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)

    items = items[0].split() # getting the mails id

    for emailid in items:
        resp, data = m.fetch(emailid, "RFC822") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

        print '[Mail]\t\t', mail["Subject"]
        if "<" in mail["from"]:
          cleanemail = mail["from"].split("<")[1].split(">")[0]
          del(mail["from"])
          mail["from"] = cleanemail

        Branch(mail)

#    print showme(mail)
