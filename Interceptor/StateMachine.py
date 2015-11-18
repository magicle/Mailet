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
        print("at cookie_pending1 of StateMachine")
        self.client_state == "cookie_2"
        (result, randcode) = twoparty.AuthSplit(data)

        return (b"\x00" + result, randcode)
#        return (b"\x00" + data, randcode)
      elif self.client_state == "cookie_2":
        print("at cookie_pending2 of StateMachine")
#        result = twoparty.AuthSplit(self.text + data)
        result = self.text + data
        return b"\x00" + result
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
