import twoparty


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
  def IsPick(self):
    if self.http_data != None:
      return True
    else:
      return False
    
  def SetState(self, state):
    self.client_state = state

  # take in data, set state 
  # (client_state, self.H, self.pad)

  def Run(self, data, side):
    if side == "server":
      if self.client_state == "cookie_pending1":
        self.text = data
        self.client_state == "cookie_pending2"
        return None
      elif self.client_state == "cookie_pending2":
        result = twoparty.AuthSplit(self.text + data)
        return b"\x00" + result
      else:
        return data

    if side == "client":
      if data[0] == 5:
        self.SetState("check")
        if self.http_data != None:
          twoparty.Check(data[1:], self.http_data)
      elif data[0] == 4:
        self.SetState("retweet")
        return None
      elif data[0] == 3:
        self.SetState("post")
        return None
      elif data[0] == 2:
        self.SetState("cookie")
        return None
      elif data[0] == 0:
        self.H = data[1:]
        return {'reply': b"\x00HH"}
      elif data[0] == 1:
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
          result = twoparty.CookieSession(self.H, data[1:], self.text, sys.argv[1], sys.argv[2])
          self.client_state = "cookie_pending1"
        elif self.client_state == "post":
          result = twoparty.Post(self.H, self.pad, self.http_data, self.arg1, self.arg2, "Post")
        elif self.client_state == "retweet":
          result = twoparty.Post(self.H, self.pad, self.http_data, self.arg1, self.arg2, "Retweet")
        else:
          result = twoparty.GCM(self.H, self.pad, self.http_data, self.arg1, self.arg2)
        return {'forward': result}
