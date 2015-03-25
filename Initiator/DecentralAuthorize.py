import TwitterAuth
import twoparty
import os
import time
import sys, subprocess




class DecentAuthMachine:

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.Prepare()
  
  def Prepare(self):
    url = TwitterAuth.AuthLink()
    self.authen_token = TwitterAuth.AuthenToken(url)
    self.oa_token = url.split("=")[1].strip("\n")
    
    # create temp file for param pass and signaling
    # require Prepare() run just before Authorize()
    proc = subprocess.Popen(["touch", "temp"])
    proc.wait()




  # do decentral Authorize
  # return credential; if failed return None
  def Authorize(self, addr):
    
    # delete PlainMsg if exists
    if os.path.isfile("/tmp/PlainMsg"):
      os.remove("/tmp/PlainMsg")
    
    # fork
    pid = os.fork()
    if pid != 0:
      response = TwitterAuth.TwitterPost(self.authen_token, self.oa_token, self.username, self.password.decode('hex'), addr)
      code = TwitterAuth.Response2Code(response)
      
      os.waitpid(pid, 0)
      
      credential = None
      # success mark
      if len(code) != 0:
        credential = TwitterAuth.Code2Access(code)
        print "[Authorize]\tAuthorize Success"
      else:
        print "[Authorize]\tAuthorize Fail"
      
      os.remove("/tmp/PlainMsg")
      return credential
    else:
      # check whether proxy is online by checking temp file
      while True:
        if not os.path.isfile("temp"):
          break
      twoparty.TwoParty(self.password)
      sys.exit(0)



 



