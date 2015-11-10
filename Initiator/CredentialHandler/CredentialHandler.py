class CredentialHandler:
  credential = dict()

  def __init__(self):
    f = open("credential", "r")
    for item in f.readlines():
      # strip the \n
      item = item.rstrip("\n")
      email = item.split(":")[0]

      access_token = item.split(":")[1].split()[0]
      access_token_secret = item.split(":")[1].split()[1]

      # add to credential dict
      CredentialHandler.credential.setdefault(email, [])
      CredentialHandler.credential[email].append(access_token)
      CredentialHandler.credential[email].append(access_token_secret)

  def UpdateCredential(self, email, access_key, access_secret):
    if email in CredentialHandler.credential.keys():
      del(CredentialHandler.credential[email][:])
      CredentialHandler.credential[email].append(access_key)
      CredentialHandler.credential[email].append(access_secret)
    else:
      CredentialHandler.credential.setdefault(email, [])
      CredentialHandler.credential[email].append(access_key)
      CredentialHandler.credential[email].append(access_secret)
    
    # write back for update
    f = open("credential", "w")
    for key in CredentialHandler.credential.keys():
      f.write(key + ":")
      for item in CredentialHandler.credential[key]:
        f.write(item + " ")
      f.write("\n")
    f.close()
  
  def GetCredential(self, email):
    if email not in CredentialHandler.credential.keys():
      return None
    else:
      return CredentialHandler.credential[email]


