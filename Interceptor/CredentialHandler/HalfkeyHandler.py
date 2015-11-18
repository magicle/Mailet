class HalfkeyHandler:
  Halfkey = dict()

  def __init__(self):
    f = open("./CredentialHandler/HalfCredential", "r")
    for item in f.readlines():
      # strip the \n
      item = item.rstrip("\n")
      email = item.split(":")[0]

      account = item.split(":")[1].split()[0]
      password = item.split(":")[1].split()[1]

      # add to credential dict
      HalfkeyHandler.Halfkey.setdefault(email, [])
      HalfkeyHandler.Halfkey[email].append(account)
      HalfkeyHandler.Halfkey[email].append(password)

  def UpdateHalfkey(self, email, account, password):
    if email in HalfkeyHandler.Halfkey.keys():
      del(HalfkeyHandler.Halfkey[email][:])
      HalfkeyHandler.Halfkey[email].append(account)
      HalfkeyHandler.Halfkey[email].append(password)
    else:
      HalfkeyHandler.Halfkey.setdefault(email, [])
      HalfkeyHandler.Halfkey[email].append(account)
      HalfkeyHandler.Halfkey[email].append(password)

    # write back in update
    f = open("./CredentialHandler/HalfCredential", "w")
    for key in HalfkeyHandler.Halfkey.keys():
      f.write(key + ":")
      for item in HalfkeyHandler.Halfkey[key]:
        f.write(item + " ")
      f.write("\n")
    f.close()

  def GetHalfkey(self, email):
    if email not in HalfkeyHandler.Halfkey.keys():
      return None
    else:
      return HalfkeyHandler.Halfkey[email]





