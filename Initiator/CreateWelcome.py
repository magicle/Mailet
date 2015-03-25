import sys, os



# read ServerList from ../ServerList file

fd_serverlist = open("", "r")

ServerList = list()

for EachLine in fd_serverlist.readlines():
  ServerList.append(EachLine.strip('\n'))

fd_serverlist.close()

# create welcome page

fd_welcome = open("welcome.html", "r+")

WelcomeLines = fd_welcome.readlines()
fd_welcome.seek(0)
for EachLine in WelcomeLines:
  if "ServerList = " in EachLine:
    # create ServerList line

    Line = ""
    for EachServer in ServerList:
      Line = Line + "\"" + EachServer + "\"" + ","
    Line = Line.strip(",")
    Line = "  var ServerList = [" + Line + "];\n"
    fd_welcome.write(Line)
  else:
    fd_welcome.write(EachLine)

fd_welcome.close()




