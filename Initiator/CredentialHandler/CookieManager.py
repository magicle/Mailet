import sys, os
import binascii


class CookieManager:

  def __init__(self, direct):
    self.direct = direct

  def Read(self, username):
    cookiedir = os.listdir(self.direct)
    
    # search cookie
    if username in cookiedir:
      f = open(self.direct + username, 'r')
      cookie = f.read()
      f.close()

      # unhexlify the auth_token
      temp = cookie.split("auth_token=")
      auth_token = temp[1].rstrip(';')
      cookie = temp[0] + "auth_token=" + binascii.unhexlify(auth_token).decode('utf-8') + ";"
      return cookie
    else:
      print("error: cookie not found!")

  def Write(self, username, cookie):
    f = open(self.direct + username, 'w')
    f.write(cookie)
    f.close()

