#!/usr/bin/python
# -*- coding: utf-8 -*-
# j3nnn1 

import sys
import tweepy

#sys.defaultencoding('utf-8')
#reload(sys)

search_tweets = tweepy.api.search('perl')
print 'tamaño del arreglo devuelto:' + str(len(search_tweets))
for i, tweet in enumerate(search_tweets):
    print 'numero: '+str(i)
    print tweet.text

#print 'Public timeline:.'

public_tweets = tweepy.api.public_timeline()
print 'tamaño del arreglo devuelto:' + str(len(public_tweets))


for i, tweet in enumerate(public_tweets):
    print 'numero: '+str(i)
#
    userpublic = tweet.user
    print userpublic.id
    print str(userpublic.screen_name)
    print tweet.text
    print str(userpublic.profile_image_url)
   


    #print type(tweet)
    #print dir(tweet)
    #print tweet.profile_image_url
#

#autenticando en twitter
#
#auth  =  tweepy.OAuthHandler(consumer_token, consumer_secret)
#auth.set_access_token(key, secret)
#api = tweepy.API(auth)
#api.update_status('porque recordar es vivir.. viendo --> i dream of jeannie ')

#user = tweepy.api.get_user('j3nnn1')

#print str(user.id)
#print str(user.profile_image_url)
#print str(user.status.text)


print 'User time line:.'

usertl = tweepy.api.user_timeline('j3nnn1')


for i,tweet in enumerate(usertl):
    print 'tweet numero : '+str(i)
    print tweet.text
    print 'foto:'
    print tweet.user.profile_image_url 
    print 'nickname:'
    print tweet.user.screen_name
    print 'nombre:'
    print tweet.user.name



