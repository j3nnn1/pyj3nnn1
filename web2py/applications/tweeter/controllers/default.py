# -*- coding: utf-8 -*- 

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
    import tweepy
    
    u=tweepy.api.get_user('joseflunap')
    publico=tweepy.api.public_timeline()
   
    return dict(usuario=u,tweets=publico)
