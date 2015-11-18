import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.MIMEBase import MIMEBase
from email import Encoders

def UserlistPage(Flist):
  page = ""
  wspace = "&nbsp;&nbsp;&nbsp;&nbsp;"
  
  for each in Flist.keys():
    item = Flist[each]
    page = page + "<p>" + item['name'] + "(<em>@" + item['screen_name'] + "</em>)" + wspace + "Description: " + ("None" if item['description']=="" else item['description']) + "</p>"
  return page

def MsgHomepage(myemail):
  href = "mailto:" + myemail + "?subject="
  wspace = "&nbsp;&nbsp;"
  head_msg = "<h2>Mailet: Email Your Tweets</h2>"
  mytweet_msg = "<a href=\"" + href + "mytweet" + "\">[My Tweets]</a>"

  post_msg = "<a href=\"" + href + "posttweet" + "\">[Post a Tweet]</a>"
  search_msg = "[Search Tweets]: " + "<a href=\"" + href + "searchbyname" + "\">by name</a>" + ", " +  "<a href=\"" + href + "searchbykey" + "\">by keyword</a>"
  
  # following and follower
  following_msg = "<a href=\"" + href + "following:self" + "\">[Following</a>"
  follower_msg = "<a href=\"" + href + "follower:self" + "\">Follower]</a>"
  return head_msg + "<p>" + mytweet_msg + wspace  + post_msg + wspace + following_msg + ", " + follower_msg + wspace + search_msg + "</p>" + "<br>"



def TweetHtml(Tweet, ServerEmail, isme):
  wspace = "&nbsp;&nbsp;&nbsp;"
  TweetId = Tweet['id_str']
  TweetText = "<em>" + Tweet['screen_name'] + "</em>" + ": " + unicode(Tweet['text'])
  reply_msg = "<a href=\"mailto:" + ServerEmail + "?subject=tweetreply:" + TweetId + "\">reply</a>" 
  retweet_msg = "<a href=\"mailto:" + ServerEmail + "?subject=retweet:" + TweetId + "\">retweet</a>"
  delete_msg = "<a href=\"mailto:" + ServerEmail + "?subject=deletetweet:" + TweetId + "\">delete</a>"
  if isme != True:
    return "<p>" + TweetText + wspace + reply_msg + wspace + retweet_msg + "</p>"
  else:
    return "<p>" + TweetText + wspace + reply_msg + wspace + delete_msg + "</p>"



def send_mail(send_from, password, send_to, subject, text, files=None, server="smtp.gmail.com:587"):
#    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    
    msg.set_charset('utf8')
    msg.attach(MIMEText(text, 'html', 'UTF-8'))
    
    if files != None:
      for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=welcome.html')
        msg.attach(part)

    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login(send_from, password)

    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
