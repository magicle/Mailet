# provide email related functionality.

# user send email, whose subject should be: "request", body include:
# "yourskypename".

import time
import email, imaplib, os, random, sys
import smtplib
import subprocess



#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email import Encoders



sys.path.append(os.getcwd() + "/CredentialHandler/")
sys.path.append(os.getcwd() + "/twitter_api/")

from HalfkeyHandler import HalfkeyHandler
from CredentialHandler import CredentialHandler
from TwitterHandler import TwitterHandler
import UtilEmail 

global half
half = HalfkeyHandler()

global credential
credential = CredentialHandler()

global Eaddr,passwd
Eaddr = "magiclamp1000@gmail.com"
passwd = "202154215471"


os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'


def Branch(mail):
    global Eaddr, passwd
    if ":" not in mail["Subject"]:
      if mail["Subject"] == "password":
        PassWord(mail)
        return 1
      elif mail['Subject'] == "mytweet":
        MyTweet(mail)
        return 1
      elif mail['Subject'] == "posttweet":
        PostTweet(mail)
        return 1
      elif mail['Subject'] == "test":
        Test(mail)
        return 1
      elif mail['Subject'] == "searchbyname":
        SearchByName(mail)
        return 1
      elif mail['Subject'] == "searchbykey":
        SearchByKey(mail)
        return 1
    else:
      command = mail['Subject'].split(":")[0]
      param = mail['Subject'].split(":")[1]
      
      if command == "retweet":
        ReTweet(mail, param)
        return 1
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "welcome to Mailet", "Mailet", ["welcome.html"])
      


def ReTweet(mail, param):

  emailaddr = mail['from']

  # retweet 
  FNULL = open(os.devnull, "w")
  while(True):
    proc = subprocess.Popen(['python3.4', 'post_retweet.py', emailaddr, param, "retweet"])
#    proc = subprocess.Popen(['python3.4', 'post_retweet.py', emailaddr, param, "retweet"], stdout=FNULL, stderr=FNULL)
    proc.wait()
    print "[post_tweet: returncode]\t\t", proc.returncode
    if proc.returncode == 1:
      MailBack(mail['from'], "success", "post success")
      break
  return 1
  
def SearchByKey(mail):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  KeyWord = BodyOneLine(mail)
  TweetList = Thandle.SearchByKey(KeyWord)

  Homepage = UtilEmail.MsgHomepage(Eaddr)
  Tweetpage = ""

  for item in TweetList:
    Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, False)

  UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Search By Keyword", Homepage + Tweetpage)
  return 1


def SearchByName(mail):
  global credential, Eaddr, passwd
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    MailBack(mail['from'], "Error: the provided account never exists!", "Fail")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  username = BodyOneLine(mail).split()[0]
  TweetList = Thandle.SearchTweetByUser(username)
  
  Homepage = UtilEmail.MsgHomepage(Eaddr)
  Tweetpage = ""

  for item in TweetList:
    Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, False)
  
  UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Search By Name", Homepage + Tweetpage)
  return 1

def PostTweet(mail):
  emailaddr = mail['from']
  msg = BodyOneLine(mail)

  # post
  FNULL = open(os.devnull, "w")
  while(True):
    proc = subprocess.Popen(['python3.4', 'post_retweet.py', emailaddr, msg, "post"])
#    proc = subprocess.Popen(['python3.4', 'post_retweet.py', emailaddr, msg, "post"], stdout=FNULL, stderr=FNULL)
    proc.wait()
    print "[post_tweet: returncode]\t\t", proc.returncode
    if proc.returncode == 1:
      MailBack(mail['from'], "success", "post success")
      break
  return 1

def MyTweet(mail):
  global credential, Eaddr, passwd
  mycre = credential.GetCredential(mail['from'])
  if mycre != None:
    Thandle = TwitterHandler(mycre[0], mycre[1])
    TweetList= Thandle.MyTimeLine(20)
    
    Homepage = UtilEmail.MsgHomepage(Eaddr)
    Tweetpage = ""
    for item in TweetList:
      Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, True)
    
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] My Tweets", Homepage + Tweetpage)

  else:
    MailBack(mail['from'], "Error: the provided account never exists!", "Fail")




def Test(mail):
  global Eaddr
  MailBack(mail["from"], UtilEmail.MsgHomepage(Eaddr), "[Mailet] Homepage")

    
  
# stores the half credential
def PassWord(mail):
  global half, Eaddr
  mmail = mail["from"]
  UnamePass = BodyOneLine(mail)

  account = UnamePass.split()[0]
  password = UnamePass.split()[1]
  
  half.UpdateHalfkey(mmail, account, password)

  
  # get cookie
  while(True):
    FNULL = open(os.devnull, 'w')
#    proc = subprocess.Popen(['python3.4', 'example_cookie.py', mmail], stdout=FNULL, stderr=FNULL)
    proc = subprocess.Popen(['python3.4', 'example_cookie.py', mmail])
    proc.wait()
    print '[cookie_split: return code]\t\t', proc.returncode
    if proc.returncode == 1:
      break
  MailBack(mmail, "Success for " + Eaddr, "half credential received, cookie success")


def BodyOneLine (msg):  
  maintype = msg.get_content_maintype()
  if maintype == 'multipart':
    for index, part in enumerate(msg.walk()):
      if index == 1:
        result = part.get_payload().split("\n")[0]

  elif maintype == 'text':
    result =  msg.get_payload().split("\n",1)[0]
  return result.strip("\n\r")





# send html email
def MailBack(Who, Msg, Subject):
    global Eaddr, passwd
    fromaddr = Eaddr
    toaddrs  = Who
    username = Eaddr.split("@")[0]
    password = passwd

    headers = ["from: "+ fromaddr, "subject: "+ Subject]
    headers.append("MIME-Version: 1.0")
    headers.append("Content-type: text/html")
    headers = "\r\n".join(headers)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)

#    server.sendmail(fromaddr, toaddrs, Msg)
    server.sendmail(fromaddr, toaddrs, headers + "\r\n\r\n" + Msg)
    server.quit()



def init():
  
  
  if not os.path.exists("HalfCredential"):
    f = open("HalfCredential", "w")
    f.write("\n")
    f.close()
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

        print "[Mail]\t\t", mail["Subject"]
        if "<" in mail["from"]:
          cleanemail = mail["from"].split("<")[1].split(">")[0]
          del(mail["from"])
          mail["from"] = cleanemail
            
        Branch(mail)

#    print showme(mail)
