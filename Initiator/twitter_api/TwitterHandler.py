## twitter handler

import sys, os
from TwitterAPI import TwitterOAuth, TwitterAPI
import pprint



class TwitterHandler:
  consumer_key = "wgnkAhlsmOsLugGSbd5QGI45a"
  consumer_secret = 'LHMwiNVVr1cvR0xFFCVNYYpLltWWAtdppiF2SmDqdYB3KZKrZs'

  def __init__(self, access_token_key, access_token_secret):
    self.access_token_key = access_token_key
    self.access_token_secret = access_token_secret


  def GetFollowingName(self, who=None):
    ids = self.GetFollowingId(who) 
    return self.Id2UserInfo(ids)

  def GetFollowerName(self, who=None):
    ids = self.GetFollowerId(who)
    return self.Id2UserInfo(ids)


  def Id2UserInfo(self, ids):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    Fdict = dict()
    r = api.request('users/lookup', {'user_id':ids})
    for item in r:
      Fdict[item['id_str']] = {'screen_name':item['screen_name'], 'description':item['description'], 'name':item['name']}
    return Fdict 
  
  def GetFollowerId(self, who=None):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('followers/ids', {'screen_name':who})
    ids = list()
    for item in r:
      if "ids" in item:
        ids = item['ids'] + ids
    return ids

  def GetFollowingId(self, who=None):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('friends/ids', {'screen_name':who})
    ids = list()
    for item in r:
      if "ids" in item:
        ids = item['ids'] + ids
    return ids
      


  def SearchTweetByUser(self, User):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('statuses/user_timeline', {'count':20, 'screen_name':User})

    TweetList = list()
    for item in r:
      if "text" in item and "id_str" in item:
        TweetList.append({"text":item['text'], "id_str":item['id_str'], "screen_name":item['user']['screen_name']})
    return TweetList

  def Tweet2User(self, TweetNum):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('statuses/show/:' + TweetNum, {'id':TweetNum})
    for item in r:
      if "user" in item and "screen_name" in item['user']:
        return item["user"]['screen_name']
    return False

  def DeleteTweet(self, TweetNum):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('statuses/destroy/:' + TweetNum, {'id':TweetNum})
    if r.status_code == 200:
      return True
    else:
      return False


  def ReplyTweet(self, TweetNum, ReplyMsg):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    Username = self.Tweet2User(TweetNum)
    ReplyMsg = "@" + Username + " " + ReplyMsg
    r = api.request('statuses/update', {'status':ReplyMsg, 'in_reply_to_status_id':TweetNum})
    if r.status_code == 200:
      return True
    else:
      return False

  def PostTweet(self, Msg):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('statuses/update', {'status':Msg})
    if r.status_code == 200:
      return 1
    else:
      return 0

  def ReTweet(self, TweetNum):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    print("here")
    r = api.request('statuses/retweet/:' + TweetNum, {'id':TweetNum})
    if r.status_code == 200:
      return True
    else:
      return False


  def MyTimeLine(self, count):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('statuses/user_timeline', {'count': count}) 
    TweetList = list()
    for item in r:
      if "text" in item and "id_str" in item:
        TweetList.append({"text":item['text'], "id_str":item['id_str'], "screen_name":item['user']['screen_name']})

    # 
    return TweetList

  def SearchByKey(self, keyword):
    api = TwitterAPI(TwitterHandler.consumer_key, TwitterHandler.consumer_secret, self.access_token_key, self.access_token_secret)
    r = api.request('search/tweets', {'q': keyword, 'count':100})
    TweetList = list()
    for item in r:
      if "text" in item and "id_str" in item:
        TweetList.append({"text":item['text'], "id_str":item['id_str'], "screen_name":item['user']['screen_name']})
    return TweetList
