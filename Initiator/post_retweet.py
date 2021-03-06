import sys
import os
import binascii

os.environ['LD_LIBRARY_PATH'] = '/usr/local/ssl/lib/'

sys.path.append(os.getcwd() + "/CredentialHandler/")

from CookieManager import CookieManager
from TwitterConnector import TwitterConnector
from HalfkeyHandler import HalfkeyHandler

Cookie = CookieManager("./cookie/")
half = HalfkeyHandler()
#auth= "5c5956060f16435550415f584a140d5412145b4f5243034c560c145a530f4a034a0c5f095c1c0756"
##
#auth = binascii.unhexlify(auth)
#auth = auth.decode('utf8')
##
#cookiecontent = "_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGwTnFBNAToMY3NyZl9p%250AZCIlMWRjNzQ0NjRhZTRiNjc2MjUzYWY4MGU5YjA2Yjc4MDQ6B2lkIiUzNzk3%250ANjdhMTFhOWZmNWE3ZTk4NDE2YzdjMThhMzZmOA%253D%253D--1227b68055256262155b52bf7b149fcb2021d60c;twid=\"u=3029045577\";guest_id=v1%3A143157651543508870;auth_token=" + auth + ";"
##Cookie.Write('skymomo10@163.com', cookiecontent)
##




# convert emailaddr to username
username = half.GetHalfkey(sys.argv[1])[0]
out = Cookie.Read(username)

print("cookie is: ", out)
con = TwitterConnector(1)
con.SetCookie(out)
#con.SetCookie(cookiecontent)

if sys.argv[3] == "post":
  con.InitConn('post', {'post':sys.argv[2]})
elif sys.argv[3] == "retweet":
  con.InitConn('retweet', {'retweet':sys.argv[2]})
else:
  sys.exit(0)
 
print("InitConn finished")

con.Start()
print("Start finished")

con.PickThenReconstruct()
print("PickThenReconstruct finished") 

res = con.ReceiveResponse()
print("ReceiveResponse finished")

if res == None:
  sys.exit(0)
else:
  sys.exit(1)


