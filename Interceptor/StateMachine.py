import twoparty
import Constants

# input: TLS data (client)
# output: TLS data (to relay)
# keep states

class StateMachine:

  def __init__(self, arg1, arg2):
    self.arg1 = arg1
    self.arg2 = arg2
    self.client_state = None
    self.H = None
    self.pad = None
    self.http_data = None

    self.COOKIE_START_POS = Constants.COOKIE_START_POS + len(self.arg2)
    print("self.COOKIE_START_POS:", self.COOKIE_START_POS)


  # whether ready for pick & check
  def IsReadyPick(self):
    if self.http_data != None:
      return True
    else:
      return False
    
  def SetState(self, state):
    self.client_state = state
  
  def GetState(self):
    return self.client_state
  # take in data, set state 
  # (client_state, self.H, self.pad)

  def Run(self, data, side):
    if side == "server":
      if self.client_state == "cookie_1":
        self.randcode = b""
        self.client_state = "cookie_2"
        print("at cookie_pending1 of StateMachine")
        self.cookie_length = len(data) - 13
        print("self.cookie1_length", self.cookie_length)
        if self.cookie_length <= self.COOKIE_START_POS:
          return b"\x00" + data 
        else:
          (result, randcode) = twoparty.AuthSplit(data, self.COOKIE_START_POS)
          self.randcode = randcode
          return b"\x00" + result 
      elif self.client_state == "cookie_2":
        print("at cookie_pending2 of StateMachine")
        if self.cookie_length <= self.COOKIE_START_POS:
          pos = self.COOKIE_START_POS - self.cookie_length
        else:
          pos = 0

        (result, randcode) = twoparty.AuthSplit(data, pos)
        self.randcode = self.randcode + randcode
        return b"\x00" + result
#        return b"\x00" + data

      else:
        return data

    if side == "client":
      if data[0] == Constants.CONTROL_CODE['check_int']:
        self.SetState("check")
        if self.http_data != None:
          twoparty.Check(data[1:], self.http_data)
      elif data[0] == Constants.CONTROL_CODE['retweet_int']:
        self.SetState("retweet")
        return None
      elif data[0] == Constants.CONTROL_CODE['post_int']:
        self.SetState("post")
        return None
      elif data[0] == 2:
        self.SetState("cookie")
        return None
      elif data[0] == Constants.CONTROL_CODE['H_int']:
        self.H = data[1:]
        return {'reply': b"\x00HH"}
      elif data[0] == Constants.CONTROL_CODE['pad_int']:
        self.pad = data[1:]
      elif data[0] == Constants.CONTROL_CODE['auth_pos_int']:
        self.rand_pos = int(data[1:].decode('utf-8')) - self.COOKIE_START_POS
        print("self.rand_pos", self.rand_pos)
        print("auth_pos", int(data[1:].decode('utf-8')))
        return {'record': self.rand_pos} 
      elif b"\x17\x03\x03" in data:
        self.http_data = data
        return None
      else:
        # non-special data: no change
        return {'forward': data}
    
      # if ready to recompute
      if self.client_state != None and self.H != None and self.http_data != None and self.pad != None:
        if self.client_state == "cookie":
          result = twoparty.CookieSession(self.H, self.pad, self.http_data, self.arg1, self.arg2)
          print("result in StateMachine of cookie:", result)
          self.client_state = "cookie_1"
        elif self.client_state == "post":
          result = twoparty.Post(self.H, self.pad, self.http_data, self.arg1, self.arg2, "Post")
        elif self.client_state == "retweet":
          result = twoparty.Post(self.H, self.pad, self.http_data, self.arg1, self.arg2, "Retweet")
        else:
          result = twoparty.GCM(self.H, self.pad, self.http_data, self.arg1, self.arg2)
        return {'forward': result}
