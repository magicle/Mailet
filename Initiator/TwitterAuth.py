import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from TwitterAPI import TwitterAPI
import httplib2
import sys
from urllib import urlencode
import urllib
import subprocess
import os



consumer_key = 'wgnkAhlsmOsLugGSbd5QGI45a'
consumer_secret = 'LHMwiNVVr1cvR0xFFCVNYYpLltWWAtdppiF2SmDqdYB3KZKrZs'

request_key = ""
request_secret = ""


def Code2Access(code):
  print "[TwitterAuth]\tCode to Access Token"
  global consumer_key, consumer_secret, request_key, request_secret
  oauth = OAuth1(
      consumer_key,
      consumer_secret,
      request_key,
      request_secret,
      verifier=code)
  r = requests.post(url='https://api.twitter.com/oauth/access_token', auth=oauth)
  credentials = parse_qs(r.content)
  access_token_key = credentials.get('oauth_token')[0]
  access_token_secret = credentials.get('oauth_token_secret')[0]
  return [access_token_key, access_token_secret]




def ExtractEncInput(response):
  Res = []
  for index, item in enumerate(response):
    if "rec->input" in item:
      Res.append(item)

  return Res

def ExtractPlainText(response):
  pattern = "50 4f 53 54"
  RecInput = ExtractEncInput(response)
  for item in RecInput:
    if item.startswith(pattern, 12, 30):
      HexString = item.split('=')[1].split(" ")
      Res = ""
      for item in HexString:
        Res = Res + item
      return Res.strip("\n")


def TwitterPost(authen, oau, username, password, addr):
  print "[TwitterAuth]\tPOST to Twitter..."

  userfield = "session[username_or_email]"
  passfield = "session[password]"
  data1 = {'authenticity_token':authen, 'oauth_token':oau}
  data2 = {userfield:username}
  data3 = {passfield:password}
  data = urlencode(data1) + "&" + urlencode(data2) + "&" + urllib.quote(passfield) + "=" + password

  # param pass
  f = open("temp", "w")
  f.write(data)
  f.close()

  p = subprocess.Popen(['python3.3', 'connect.py', addr, oau], stdout=subprocess.PIPE)
  Res = p.stdout.readlines()


  print "[TwitterAuth]\tPOST Finished" 
  return Res

def Response2Code(response):
  for item in response:
    if "<code>" in item:
      return item.split("code>")[1].strip('</')






def AuthenToken(url):
  
  h = httplib2.Http(".cache")
  r, content = h.request(url, "GET")

  # extract authen token
  for item in content.split('\n'):
    if "form_authenticity_token" in item:
      return item.split("=")[1].strip(" ;\'\n")
  return 0





def AuthLink():
  print "[TwitterAuth]\tCreate Authorization Link"
  global consumer_key, consumer_secret, request_key, request_secret

  # obtain request token
  oauth = OAuth1(consumer_key, client_secret=consumer_secret)
  r = requests.post(url='https://api.twitter.com/oauth/request_token', auth=oauth)
  #print r.content
  credentials = parse_qs(r.content)
  request_key = credentials.get('oauth_token')[0]
  request_secret = credentials.get('oauth_token_secret')[0]


  # obtain authorization from resource owner
#  print('https://api.twitter.com/oauth/authorize?oauth_token=%s' % request_key)
  return 'https://api.twitter.com/oauth/authorize?oauth_token=' + request_key
