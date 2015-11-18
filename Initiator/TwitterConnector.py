import binascii


import urllib.request 
import urllib.parse
import socket, ssl, pprint
import sys, urllib
import io
import gzip
import select
import time, os
import subprocess
import iv
import binascii
import datetime

from TLSConnector import TLSConnector

# TwitterConnector is a child of TLSConnector
# HTTP(s) level abstraction
# InitConn:       layout the HTTP content

class TwitterConnector(TLSConnector):
  HeaderConstant = "Host: twitter.com\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"


  def __init__(self, num):
    super().__init__(num)
  

  def AuthenToken(self):
    
    x = urllib.request.urlopen('https://twitter.com/intent/tweet')
    r = x.getheader('Set-Cookie')
    content = x.read()
    # extract session id and guest id
  
    for each_field in r.split(";"):
      # session id
      if "_twitter_sess" in each_field:
        sess = each_field.split("=")[1]
      if "guest_id" in each_field:
        guest_id = each_field.split("guest_id=")[1]
 
    # extract authen token
    for item in content.split(b'\n'):
      if b"authenticity_token" in item and b"value=" in item:
        authen = item.split(b"value=")[1].strip(b" ;\"\n>")
    
    return (sess, guest_id, authen.decode('utf-8')) 
  


  def SetCookie(self, cook):
    self.cookie = cook 


  # Init Connection: category, parameters
  # arg is a list
  def InitConn(self, category, arg):
    self.category = category

    authen_token = "1327c384700677b5798693bad74ae473cee0601f"
    # parameters 
    

    # category: post
    if category == "post":
      post = "repost_after_login=%2Fintent%2Ftweet&authenticity_token=" + authen_token + "&status=" + arg['post']
      header1 = "POST /intent/tweet HTTP/1.1\r\n"
      header2 = "Referer: https://twitter.com/intent/tweet\r\n" + "cookie: " + self.cookie + "\r\n"
      header3 = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"
      content = header1 + self.HeaderConstant + header2 + header3 + post
    
    
    # category: retweet 
    elif category == "retweet":
      post = "tweet_id=" + arg['retweet'] + "&authenticity_token=" + authen_token + "&id=" + arg['retweet'] + "&commit=Retweet"
      header1 = "POST /intent/retweet HTTP/1.1\r\n"
      header2 = "Referer: https://twitter.com/intent/retweet?tweet_id=" + arg['retweet'] + "\r\n" + "cookie: " + self.cookie + "\r\n"
      header3 = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"
      content = header1 + self.HeaderConstant + header2 + header3 + post



    # category: cookie
    elif category == "cookie":
      while True:
        (self.sess, self.guest_id, self.authen_token) = self.AuthenToken()

        print("sess length:", len(self.sess))
        # pick the sess with 285 length
        if len(self.sess) == 285:
          break
      # username & password
      # for test: 
      # cred1: 48156b6211547a190871
      # cred2: 2e74080765321b7a6d05
      username = urllib.parse.quote(arg['username'])
      password = binascii.unhexlify(arg['passcode']).decode('utf-8')

      cookie = "_twitter_sess=" + self.sess + ";" + "guest_id=" + self.guest_id + ";"
      post = "repost_after_login=%2Fintent%2Ftweet&authenticity_token=" + self.authen_token + "&status=say3&session%5Busername_or_email%5D=" + username + "&session%5Bpassword%5D=" + password
      header1 = "POST /intent/sessions HTTP/1.1\r\n"
      header2 = "Referer: https://twitter.com/intent/tweet\r\n" + "cookie: " + cookie + "\r\n"
      header3 = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"
      content = header1 + self.HeaderConstant + header2 + header3 + post

    # invalid category
    else:
      print("InitConn: Invalid Parameters")

    self.SetContent(content)
  def ReceiveResponse(self):
    if self.category == "cookie": 
      (auth_token, twid) = super().ReceiveResponse()
      if auth_token != None:
        cookie = "_twitter_sess=" + self.sess + ";" + twid +";" + "guest_id=" + self.guest_id + ";" + "auth_token=" + auth_token.decode('utf-8') + ";"
        return cookie
      else:
        return None
    else:
      res = super().ReceiveResponse()
      return res
