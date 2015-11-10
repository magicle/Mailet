import binascii

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


  def SetCookie(self, cook):
    self.cookie = cook 


  # Init Connection: category, parameters
  # arg is a list
  def InitConn(self, category, arg):
    self.category = category

    authen_token = "0327c384700677b5798693bad74ae473cee0601f"
    # parameters 
    
    # category: post
    if category == "post":
      post = "repost_after_login=%2Fintent%2Ftweet&authenticity_token=" + authen_token + "&status=" + arg['post']
      header1 = "POST /intent/tweet HTTP/1.1\r\n"
      header2 = "Referer: https://twitter.com/intent/tweet\r\n" + "cookie: " + self.cookie + "\r\n"
      header3 = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"
      content = header1 + self.HeaderConstant + header2 + header3 + post

    elif category == "retweet":
      post = "tweet_id=" + arg['retweet'] + "&authenticity_token=" + authen_token + "&id=" + arg['retweet'] + "&commit=Retweet"
      header1 = "POST /intent/retweet HTTP/1.1\r\n"
      header2 = "Referer: https://twitter.com/intent/retweet?tweet_id=" + arg['retweet'] + "\r\n" + "cookie: " + self.cookie + "\r\n"
      header3 = "Content-Type: application/x-www-form-urlencoded\r\nContent-Length: " + str(len(post)) + "\r\n\r\n"
      content = header1 + self.HeaderConstant + header2 + header3 + post

    else:
      print("InitConn: Invalid Parameters")

    self.SetContent(content)
