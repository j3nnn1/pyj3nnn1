# -*- coding: utf-8 -*- 
import tweepy
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    user = tweepy.api.get_user('j3nnn1')
    
    dictionarytweet    = {}
    dictuser           = {'name':user.name,'image':user.profile_image_url,'status':user.status.text}
    
    tweetpublic  = tweepy.api.public_timeline()
    
    for i, tweet in enumerate(tweetpublic):
        userpublic = tweet.user
        dictionarytweet[i]={'name': userpublic.screen_name, 'status':tweet.text, 'url_pic':userpublic.profile_image_url, 'username': userpublic.name}
    
    return dict(userinfo=dictuser, public=dictionarytweet)


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
