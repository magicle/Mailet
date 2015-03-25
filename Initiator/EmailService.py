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
from ServerListHandler import InterceptorListHandler

global half
half = HalfkeyHandler()

global credential
credential = CredentialHandler()

global Eaddr,passwd
Eaddr = "magiclamp1000@gmail.com"
passwd = "202154215471"

global IntHandler

IntHandler = InterceptorListHandler()


def Branch(mail):
    global Eaddr, passwd
    if ":" not in mail["Subject"]:
      if mail["Subject"] == "password":
        PassWord(mail)
        return 1
      elif mail["Subject"] == "authorize":
        Authorize(mail)
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
      elif mail['Subject'] == "InterceptorListUpdate":
        InterceptorListUpdate(mail)
        return 1
    else:
      command = mail['Subject'].split(":")[0]
      param = mail['Subject'].split(":")[1]
      
      if command == "deletetweet":
        DeleteTweet(mail, param)
        return 1
      if command == "tweetreply":
        TweetReply(mail, param)
        return 1
      if command == "retweet":
        ReTweet(mail, param)
        return 1
      if command == "following":
        Following(mail, param)
        return 1
      if command == "follower":
        Follower(mail, param)
        return 1
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "welcome to Mailet", "Mailet", ["welcome.html"])
      
def InterceptorListUpdate(mail):
  global IntHandler
  # clear the InterceptorList first
  IntHandler.ClearAll()
  Line = BodyOneLine(mail)
  
  # if empty
  if len(Line) == 0:
    return 0
  else:
    for EachInterceptor in Line.split("|"):
      print EachInterceptor
      email_addr = EachInterceptor.split()[0]
      addr = EachInterceptor.split()[1]
      IntHandler.Update(email_addr, addr)



def Follower(mail, param):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilMail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  if param == 'self':
    Flist = Thandle.GetFollowerName()
  else:
    Flist = Thandle.GetFollowingName(param)
  Homepage = UtilEmail.MsgHomepage(Eaddr)
  FlistPage = UtilEmail.UserlistPage(Flist) 
  UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Follower List", Homepage + FlistPage)
  return 1


def Following(mail, param):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilMail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  if param == 'self':
    Flist = Thandle.GetFollowingName()
  else:
    Flist = Thandle.GetFollowingName(param)
  Homepage = UtilEmail.MsgHomepage(Eaddr)
  FlistPage = UtilEmail.UserlistPage(Flist) 
  UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Following List", Homepage + FlistPage)
  return 1

def ReTweet(mail, param):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilMail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  status = Thandle.ReTweet(param)
  if status == True:
    TweetList = Thandle.MyTimeLine(5)
    Tweetpage = ""
    for item in TweetList:
      Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, True)
    Homepage = UtilEmail.MsgHomepage(Eaddr)
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] ReTweet Success", Homepage + Tweetpage)
    return 1
  else:
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: ReTweet Fails!")
    return 0

def TweetReply(mail, param):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilMail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  status = Thandle.ReplyTweet(param, BodyOneLine(mail))
  if status == True:
    Homepage = UtilEmail.MsgHomepage(Eaddr)
    
    TweetList = Thandle.MyTimeLine(5)
    Tweetpage = ""
    for item in TweetList:
      Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, True)
    
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Reply Success", Homepage + Tweetpage)
  else:
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: reply fails!")

def DeleteTweet(mail, param):
  global credential, passwd, Eaddr
  mycre = credential.GetCredential(mail['from'])
  if mycre == None:
    UtilMail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: the provided account never exists!")
    return 0
  Thandle = TwitterHandler(mycre[0], mycre[1])
  status = Thandle.DeleteTweet(param)
  if status == True:
    TweetList = Thandle.MyTimeLine(5)
    Tweetpage = ""
    for item in TweetList:
      Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, True)
    Homepage = UtilEmail.MsgHomepage(Eaddr)
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Delete Tweet", Homepage + Tweetpage)
    return 1
  else:
    UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Fail", "Error: can not delete!")
    return 0

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
  global credential, Eaddr, passwd
  mycre = credential.GetCredential(mail['from'])
  if mycre != None:
    Thandle = TwitterHandler(mycre[0], mycre[1])
    status = Thandle.PostTweet(BodyOneLine(mail))
    if status == 1:
      Homepage = UtilEmail.MsgHomepage(Eaddr)
      TweetList = Thandle.MyTimeLine(5)
      Tweetpage = ""
      for item in TweetList:
        Tweetpage = Tweetpage + UtilEmail.TweetHtml(item, Eaddr, True)
      UtilEmail.send_mail(Eaddr, passwd, mail['from'], "[Mailet] Search By Name", Homepage + Tweetpage)

    else:
      MailBack(mail['from'], "Post Tweet Fail", "Fail")
  else:
    MailBack(mail['from'], "Error: the provided account never exists!", "Fail")

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

def Authorize(mail):
  global half, Eaddr, IntHandler
  global credential 

  to = mail['To'].split(',')
  peer = None
  for each in to:
    if Eaddr not in each:
      peer = each.strip()
  if peer == None:
    print "[error]\t\tAuthorize Fail: wrong recipent format"
    return 0
  print peer 
  peer_addr = IntHandler.GetAddr(peer)
  print peer_addr

  email = mail["from"]
  UnamePass = half.GetHalfkey(email) 
  if UnamePass != None:
    au = DecentAuthMachine(UnamePass[0], UnamePass[1])
    access_token = au.Authorize(peer_addr)

    # store credential if it exists
    if access_token != None:
      credential.UpdateCredential(email, access_token[0], access_token[1])
      # notify user
      MailBack(mail["from"], "Authorize Success!", "Success!")
      MailBack(mail["from"], UtilEmail.MsgHomepage(Eaddr), "Homepage")
    else:
      MailBack(mail["from"], "Authorize failed!", "Failed")
    
  
# stores the half credential
def PassWord(mail):
  global half, Eaddr
  mmail = mail["from"]
  UnamePass = BodyOneLine(mail)

  account = UnamePass.split()[0]
  password = UnamePass.split()[1]
  
  half.UpdateHalfkey(mmail, account, password)
  MailBack(mmail, "Success for " + Eaddr, "Partial Credential Received")


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

MailBack("mailetproject@gmail.com", "initiator", "ServerListUpdate")

while 1:
    time.sleep(2)
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
