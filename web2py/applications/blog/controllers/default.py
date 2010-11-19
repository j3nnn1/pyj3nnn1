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
    Esta vista va a obtener 3 post
    """
    # filter to join.
    perpage = 3                                  # Numero de articulos por pagina
    totalposts = db(db.articulos.id > 0).count() # contamos cuantos posts hay en la bd
    totalpages = totalposts / perpage            # division para sacar el numero de paginas
                  
    page = int(request.args(0)) if request.args(0) else 1
    limit = int(page - 1) * perpage
                         
    if totalposts > perpage and totalpages == 1 and totalpages * perpage != totalposts:
        totalpages = 2

    filtro = (db.articulos.id_usuario==db.auth_user.id)
    post = db(filtro).select(db.articulos.ALL, db.auth_user.first_name, limitby=(limit,page*perpage),orderby=~db.articulos.fecha)
    comments  = [db((db.comentarios.id_articulo == i.articulos.id)&(db.comentarios.visible == '1')).count() for i in post]
	
    return dict(post=post,totalpages=totalpages,postpage=page,comments=comments)

def about():
    """ Información sobre mi persona"""
    return dict()

def viewpost():
    if request.args(0):
        #consulta en bd de un articulo en especifico
        filtro      = ((db.articulos.id==request.args(0)) & (db.articulos.id_usuario==db.auth_user.id))
        post        = db(filtro).select(db.articulos.ALL, db.auth_user.first_name).first()

        if post:
            #creando FORM de los comentarios
            form        = SQLFORM(db.comentarios)
            form.vars.id_articulo = post.articulos.id

            #obteniendo registros de los comentarios visibles
            filtro          = ((db.comentarios.id_articulo==post.articulos.id)&(db.comentarios.visible=='1'))
            comments        = (db(filtro).select(db.comentarios.ALL, orderby=~db.comentarios.fecha)).records 
	        #print db._lastsql util para saber ultima consulta ejecutada
        else:
            redirect(URL('index'))

        if form.accepts(request.vars, session):
            response.flash ='Tu comentario ha sido publicado'
    else:
        redirect(URL('index'))

    return dict(post=post, form=form, comments=comments)

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


@auth.requires_login()
def admin():
    #listando articulos disponible 
    perpage=6
    totalposts = db(db.articulos.id > 0).count() # contamos cuantos posts hay en la bd

    totalpages = totalposts / perpage

    page=int(request.args(0)) if request.args(0) else 1
    limit = int(page - 1) * perpage

    if totalposts > perpage and totalpages == 1 and totalpages * perpage != totalposts:
        totalpages = 2

    filtro = (db.articulos.id_usuario==db.auth_user.id)
    tableart = db(filtro).select(db.articulos.ALL, limitby=(limit,page*perpage),orderby=~db.articulos.fecha).records
    #tableart = db().select(db.articulos.ALL, orderby=~db.articulos.fecha).records
    
    return dict(tableart=tableart, totalpages=totalpages, postpage=page)


@auth.requires_login()
def modifypost():

    if request.args(0):  #modificando un post
        post   = db.articulos(request.args(0)) or redirect(URL('index'))
        print post

	form = SQLFORM(db.articulos, post)

	if form.accepts(request.vars, session):
            response.flash ='Tu articulo ha sido actualizado'
	elif form.errors:
	    response.flash ='No se actualizó el artículo'

    else:
	 form=none
	 response.flash ='No seleccionó el articulo'
    
    return dict(form=form)

@auth.requires_login()
def createpost():

    #form        = SQLFORM(db.articulos) forma easy
    form = SQLFORM.factory(Field('titulo',    'string',  requires=IS_NOT_EMPTY(), required=True),
                    Field('articulo',  'text',    requires=IS_NOT_EMPTY(),required=True),
                    Field('image', 'upload'),
                    Field('etiquetas', 'string'), 
                    table_name='articulos') #las etiquetas serán separadas por coma

    if form.accepts(request.vars, session):
        #extrayendo etiquetas (@etiquetas), quitando espacios extremos, e insertando etiquetas en bd almacenado sus @ids.
        etiquetas = map(lambda x: x.strip().lower() , form.vars['etiquetas'].split(','))
        #filtro las etiquetas que ya existen en bd e inserto las nuevas
        existinbd=0
        # ids de etiquetas a asociar
        ids=[]
        #se asume que tweepy se encuentra instalada
        tweepyexist=1
        for etiqueta in etiquetas:
            try:
                ID = db(db.etiquetas.nombre==etiqueta).select(db.etiquetas.id).first()['id']
                existinbd=1
            except:
                existinbd=0

            if existinbd:
                ids.append(ID)
                existinbd=0
            else:
                ids.append(db.etiquetas.insert(nombre=etiqueta))
                
        #insertando articulo
        try:
            id_articulo = db.articulos.insert(titulo=form.vars['titulo'], articulo=form.vars['articulo'], id_usuario=auth.user.id, image=form.vars['image'])
        except: print 'database not available'
        else: print 'insert article successful'

        #insertando registro en etiquetas_articulos
        for id_etiqueta in ids:
            db.etiquetas_articulos.insert(id_etiqueta=id_etiqueta, id_articulo=id_articulo)

        try:
            import tweepy
        except ImportError:
            tweepyexist=0

        if tweepyexist: 

            filtro          = ((db.cuentas_twitter.nickname=='j3nnn1')& (db.cuentas_twitter.id==db.tokens_twitter.id_cuentas_twitter))
            #obteniendo los valores de la bd
            consumer_key    = db(filtro).select(db.tokens_twitter.consumer_key).first()['consumer_key']
            consumer_secret = db(filtro).select(db.tokens_twitter.consumer_secret).first()['consumer_secret']
            #obteniendo request token
            key             = db(filtro).select(db.tokens_twitter.token_key).first()['token_key']
            secret          = db(filtro).select(db.tokens_twitter.token_secret).first()['token_secret']
            if consumer_key and consumer_secret:
                authen  =  tweepy.OAuthHandler(consumer_key, consumer_secret)
                authen.set_access_token(key, secret)        
                if authen:
                    api = tweepy.API(authen) 
                    try:
                        #api.update_status('hey @jei_nu Feliz Noche!')
                        msg='algo publicado'
                    except:
                        msg='Tu articulo ha sido publicado en el blog y en twitter'                
        msg='Tu articulo ha sido publicado'
        response.flash = msg
    return dict(form=form)

@auth.requires_login()
def deletepost():

    if request.args(0):

	filtro = (db.articulos.id==request.args(0))	
	rows   = db(filtro).delete()

	if rows:
	    response.flash ='Tu articulo ha sido eliminado'
	else:
	    response.flash ='No existe el articulo'
	
        table = db().select(db.articulos.ALL, orderby=~db.articulos.fecha).records or "No posee Articulos."
	    
    else:
        redirect(URL('index'))

    return dict(table=table)

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

def grantcomment():
    
    if request.args(0):             #id comentario.
        if request.args(1)=='True':   #visible o no
            filtro = (db.comentarios.id==request.args(0)) 
            db(filtro).update(visible=0)
            response.flash='visibilidad del Comentario cambiada'

        elif request.args(1)=='False':
            filtro = (db.comentarios.id==request.args(0))
            db(filtro).update(visible=1)
            response.flash='visibilidad del Comentario cambiada'

        elif request.args(1)=='delete':
            filtro = (db.comentarios.id==request.args(0))
            db(filtro).delete()
            response.flash='Comentario Eliminado'

    filtro = (db.comentarios.id_articulo==db.articulos.id)
    comments = db(filtro).select(db.comentarios.ALL, db.articulos.titulo).records

    return dict(comments=comments)

@auth.requires_login()
def twitterauth():
    #cambiar a dos partes una el nickname y otra el token
    form = SQLFORM.factory(Field('nickname', requires=IS_NOT_EMPTY()),
                           Field('consumer_key', requires=IS_NOT_EMPTY()),
                           Field('consumer_secret', requires=IS_NOT_EMPTY()),
                           Field('request_token', 'password', requires=IS_NOT_EMPTY()),
                           Field('request_secret', 'password', requires=IS_NOT_EMPTY()))

    if form.accepts(request.vars, session):
        id_twitter = db.cuentas_twitter.insert(auth_user_id=auth.user.id, nickname=request.vars.nickname)
        db.tokens_twitter.insert(id_cuentas_twitter=id_twitter,
                                consumer_key=request.vars.consumer_key,
                                consumer_secret=request.vars.consumer_secret,
                                token_key=request.vars.request_token,
                                token_secret=request.vars.request_secret)
        response.flash = 'twitter añadido'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'revise los errores en formulario'
    return dict(form=form)

def twitterme():
    
    try:
        import tweepy
    except ImportError:
        tweepyexist=0
        usertl=' API no disponible'

    if tweepyexist:
        usertl = tweepy.api.user_timeline('j3nnn1')
        HTML='<ul>'
        for tweet in usertl[0:4]:
            HTML = HTML + LI(XML("<strong>@tweet.user.screen_name:</strong> tweet.text"), _class='test', _id=0)
        HTML='</ul>'
        print HTML        
    return dict(HTML=HTML)
