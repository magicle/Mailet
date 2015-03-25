class ServerListHandler:
  ServerList = dict()
  def __init__(self):
    f = open("../ServerList", "r")
    Servers = f.readlines()
    for Each in Servers:
      email = Each.rstrip("\n").split()[0]
      addr = Each.rstrip("\n").split()[1]
      ServerListHandler.ServerList[email] = addr
    f.close()
  
  def ClearAll(self):
    for each in ServerListHandler.ServerList.keys():
      del ServerListHandler.ServerList[each]


  def Update(self, email, addr):

    # if this is the new record
    ServerListHandler.ServerList[email] = addr

    f = open("../ServerList", "w")
    for Each in ServerListHandler.ServerList.keys():
      f.write(Each + " " + ServerListHandler.ServerList[Each] + "\n")
    f.close()

  def GetAddr(self, email):
    if email in ServerListHandler.ServerList.keys():
      return ServerListHandler.ServerList[email]
    else:
      return False


