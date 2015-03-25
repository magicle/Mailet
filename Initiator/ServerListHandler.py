class InterceptorListHandler:
  InterceptorList = dict()
  def __init__(self):
    f = open("InterceptorList", "r")
    Interceptors = f.readlines()
    for Each in Interceptors:
      email = Each.rstrip("\n").split()[0]
      addr = Each.rstrip("\n").split()[1]
      InterceptorListHandler.InterceptorList[email] = addr
    f.close()
  
  def ClearAll(self):
    for each in InterceptorListHandler.InterceptorList.keys():
      del InterceptorListHandler.InterceptorList[each]
    f = open("InterceptorList", "w")
    f.write("")
    f.close()


  def Update(self, email, addr):

    # if this is the new record
    InterceptorListHandler.InterceptorList[email] = addr

    f = open("InterceptorList", "w")
    for Each in InterceptorListHandler.InterceptorList.keys():
      f.write(Each + " " + InterceptorListHandler.InterceptorList[Each] + "\n")
    f.close()

  def GetAddr(self, email):
    if email in InterceptorListHandler.InterceptorList.keys():
      return InterceptorListHandler.InterceptorList[email]
    else:
      return False


