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
    # Counting tags
    tagnames = db().select(db.etiquetas.nombre)
    # filter to join.
    perpage = 3  # Numero de articulos por pagina
    # contamos cuantos posts hay en la bd
    totalposts = db(db.articulos.id > 0).count()
    # division para sacar el numero de paginas
    totalpages = totalposts / perpage
    page = int(request.args(0)) if request.args(0) else 1
    limit = int(page - 1) * perpage

    if totalposts > perpage and totalpages == 1 and totalpages * perpage != totalposts:
        totalpages = 2

    filtro = (db.articulos.id_usuario==db.auth_user.id)
    post = db(filtro).select(db.articulos.ALL, db.auth_user.first_name, limitby=(limit,page*perpage),orderby=~db.articulos.fecha)
    comments = [db((db.comentarios.id_articulo == i.articulos.id)&(db.comentarios.visible == '1')).count() for i in post]
    filtro_tags = (db.etiquetas_articulos.id_etiqueta == db.etiquetas.id)
    tags_post = [db((filtro_tags)&(db.etiquetas_articulos.id_articulo == i.articulos.id)).select(db.etiquetas.nombre) for i in post]

    return dict(post=post,
		totalpages=totalpages,
		postpage=page,
            	comments=comments,
            	etiquetas=tags_post,
            	tagnames=tagnames)


def about():
    """ Información sobre mi persona"""
    return dict()


def viewpost():
    if request.args(0):
        #consulta en bd de un articulo en especifico
        filtro = ((db.articulos.id==request.args(0)) & (db.articulos.id_usuario==db.auth_user.id))
        post = db(filtro).select(db.articulos.ALL, db.auth_user.first_name).first()
        if post:
            #creando FORM de los comentarios
            form = SQLFORM(db.comentarios)
            form.vars.id_articulo = post.articulos.id
            #obteniendo registros de los comentarios visibles
            filtro = ((db.comentarios.id_articulo==post.articulos.id)&(db.comentarios.visible=='1'))
            comments = (db(filtro).select(db.comentarios.ALL, orderby=~db.comentarios.fecha)).records
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
    # contamos cuantos posts hay en la bd
    totalposts = db(db.articulos.id > 0).count()
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
    if request.args(0):
        #obteniendo articulo
        id_articulo=request.args(0)
        post = db.articulos(id_articulo) or redirect(URL('index'))
        #obteniendo etiquetas asociadas al articulo
        filtro = (db.etiquetas_articulos.id_articulo==id_articulo) & (db.etiquetas_articulos.id_etiqueta==db.etiquetas.id)
        etiquetas=[]
        [etiquetas.append(row.nombre) for row in db(filtro).select(db.etiquetas.nombre)]
        etiquetas = ", ".join(etiquetas)
        #armando formulario
        form = SQLFORM.factory(Field('titulo', 'string', requires=IS_NOT_EMPTY(), required=True),
                         Field('articulo',  'text', requires=IS_NOT_EMPTY(), required=True),
                         Field('image', 'upload'),
                         Field('etiquetas', 'string'),
                         Field('id_articulo', readable=False, writable=False),
                         table_name='articulos') #las etiquetas serán separadas por coma

        form.vars['id_articulo']= id_articulo
        form.vars['titulo'] = post['titulo']
        form.vars['articulo'] = post['articulo']
        form.vars['image'] = post['image']
        form.vars['etiquetas'] = etiquetas
    if form.accepts(request.vars, session, keepvalues=True):
            #chequeando si las etiquetas fueron modificadas
            id_etiquetas = create_tags(form.vars['etiquetas'])
            #verificar not in en tabla etiquetas_articulos e insertando las que si estan
            for etiqueta in id_etiquetas:
                filtro = (db.etiquetas_articulos.id_articulo==form.vars['id_articulo']) & (db.etiquetas_articulos.id_etiqueta==etiqueta)
                etiquetaexist = db(filtro).select() or None
                if etiquetaexist == None:
                    db.etiquetas_articulos.insert(id_etiqueta=etiqueta, id_articulo=form.vars['id_articulo'])
            #borrando etiquetas que se eliminaron
            #not in (etiquetas)
            filtro = ((~(db.etiquetas_articulos.id_etiqueta.belongs(id_etiquetas))) & (db.etiquetas_articulos.id_articulo==form.vars['id_articulo']))
            db(filtro).delete()
            #update db post
            filtro= db.articulos.id==form.vars['id_articulo']
            ok = db(filtro).update(titulo=form.vars['titulo'], articulo=form.vars['articulo'], image=form.vars['image']) or None
            if ok: response.flash ='Tu articulo ha sido actualizado'
    elif form.errors:
        response.flash ='No se actualizó el artículo'

    return dict(form=form)


def create_tweet(titulo):
    tweepyexist = 0
    msg =''
    try:
        import tweepy
        tweepyexist = 1
    except ImportError:
        tweepyexist = 0
    if tweepyexist:
        filtro = ((db.cuentas_twitter.nickname=='j3nnn1')& (db.cuentas_twitter.id==db.tokens_twitter.id_cuentas_twitter))
        #obteniendo los valores de la bd
        consumer_key = db(filtro).select(db.tokens_twitter.consumer_key).first()['consumer_key']
        consumer_secret = db(filtro).select(db.tokens_twitter.consumer_secret).first()['consumer_secret']
        #obteniendo request token
        key = db(filtro).select(db.tokens_twitter.token_key).first()['token_key']
        secret = db(filtro).select(db.tokens_twitter.token_secret).first()['token_secret']
        if consumer_key and consumer_secret:
            authen = tweepy.OAuthHandler(consumer_key, consumer_secret)
            authen.set_access_token(key, secret)
            if authen:
                api = tweepy.API(authen)
                try:
                
                    #api.update_status("En mi blog: %s" % titulo)
                    #api.update_status("Muy buenos días!")
                    msg='Tu articulo ha sido publicado en el blog y en twitter'
                except:
                    msg='API  de twitter no disponible'
            else:
                    msg='Tu articulo ha sido publicado en el blog.'
    return msg


def create_tags(tags):
    etiquetas = map(lambda x: x.strip().lower(), tags.split(','))
    #filtro las etiquetas que ya existen en bd e inserto las nuevas
    existinbd=0
    # ids de etiquetas a asociar
    ids=[]
    id_etiqueta=""
    for etiqueta in etiquetas:
        tag = db(db.etiquetas.nombre==etiqueta).select(db.etiquetas.id).first()
        if not tag:
            id_etiqueta = db.etiquetas.insert(nombre=etiqueta)
        else:
            id_etiqueta = db(db.etiquetas.nombre==etiqueta).select(db.etiquetas.id).first()['id']
        ids.append(id_etiqueta)
    return ids


@auth.requires_login()
def createpost():
    #form        = SQLFORM(db.articulos) forma easy
    form = SQLFORM.factory(Field('titulo',    'string',  requires=IS_NOT_EMPTY(), required=True),
					Field('articulo',  'text', requires=IS_NOT_EMPTY(), required=True),
                    Field('image', 'upload'),
                    Field('etiquetas', 'string'), 
                    table_name='articulos') #las etiquetas serán separadas por coma

    if form.accepts(request.vars, session):
        #extrayendo etiquetas (@etiquetas), quitando espacios extremos, e insertando etiquetas en bd almacenado sus @ids.
        ids = create_tags(form.vars['etiquetas'])
        #insertando articulo
        try:
            id_articulo = db.articulos.insert(titulo=form.vars['titulo'], articulo=form.vars['articulo'], id_usuario=auth.user.id, image=form.vars['image'])
        except:
            print 'database not available'
        else:
            print 'insert article successful'
            redirect(URL('viewpost', args=id_articulo))
        #insertando registro en etiquetas_articulos
        [db.etiquetas_articulos.insert(id_etiqueta=i, id_articulo=id_articulo) for i in ids] # List comprehensions rocks 
        response.flash = msg = create_tweet(form.vars['titulo']) # Comentado pq necesita algun trabajo adicional

    return dict(form=form)

@auth.requires_login()
def deletepost():
    if request.args(0):
        filtro = (db.articulos.id==request.args(0))
        rows = db(filtro).delete()
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

    if request.args(0):  #id comentario.
        if request.args(1)=='True':  #visible o no
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

def getcloudtag():
	result = {} 
	count	  = db.etiquetas_articulos.id_etiqueta.count()
	group	  = db.etiquetas.nombre
	filtro	  = (db.etiquetas.id==db.etiquetas_articulos.id_etiqueta)
	etiquetas = db(filtro).select(db.etiquetas.nombre, count ,  groupby=group);
	
	for etiqueta in etiquetas:
		result[etiqueta.etiquetas.nombre] = etiqueta[count]

	return result

def showcloudtag():
	etiquetas = getcloudtag()
	cadena	  = ''
	size = 0
	for etiqueta in etiquetas.keys():
		size = getsizefont(etiquetas[etiqueta])
		cadena = "<a href='listarticlesbytag?args="+ etiqueta +"'><span style='font-size:"+str(size)+"em;'> "+ etiqueta +'</span></a>' + cadena
		
		
 	html = DIV(XML(cadena), _id='etiquetas', _class='etiquetas', _width='80', _high='100')
	return dict(html=html)

def gethighertag():
	etiquetas=getcloudtag()
	higher = 0	
	for etiqueta in etiquetas.keys():
		if etiquetas[etiqueta]>higher: 
			higher=etiquetas[etiqueta]
	return higher

def countalltags():
	etiquetas=getcloudtag()
	suma = 0	
	for etiqueta in etiquetas.keys():
		suma= suma + etiquetas[etiqueta]
	return suma

def getsizefont(s):
	higher = gethighertag()
	num    = getcountarticle()
	size   = 0
	size   = s * int(num) / int(higher)
	numtag = countalltags()
	algo = float(size)/numtag
	if (algo<1):
		size = float(size)/numtag +1
	elif(algo>=1 and algo<=2):
		size = float(size)/numtag
	else:
		size=2
	return size

def countalltag():
	etiquetas=getcloudtag()
	suma = 0	
	for etiqueta in etiquetas.keys():
		suma = suma + etiquetas[etiqueta]
			
	return suma

def getcountarticle():
	num=0
	num = int(db(db.articulos.id).count())
	return num


def listarticlesbytag():
	etiqueta =''
	result={}
	if request.get_vars['args']:
		etiqueta = request.get_vars['args']
		filtro=(db.etiquetas.nombre==etiqueta) & (db.etiquetas.id==db.etiquetas_articulos.id_etiqueta) & (db.etiquetas_articulos.id_articulo==db.articulos.id)
		arti= db(filtro).select(db.articulos.id, db.articulos.titulo, orderby=~db.articulos.fecha)
		print arti
		for art in arti:
			result[art['id']]=art['titulo']
	else:
		 redirect(URL('index'))
	return dict(result=result)

def showarchivesold():
	etiquetas = db(filtro).select(db.articulos.nombre, count ,  groupby=db.articulos.fecha.year());
	print  db().select()
	return dict(html=html)


def rss_blog():
    
    filtro = (db.articulos.id >0)
    posts = db(filtro).select(db.articulos.titulo, db.articulos.id,  db.articulos.articulo, db.articulos.fecha)
    rss =[];

    for post in posts:
        postrss = { 'title': post.titulo,
                    'link': 'http://localhost:8000/blog/default/viewpost/' + str(post.id),#  URL('viewpost', args=post.id),
                    'description': str(post.articulo[0:49]),
                    'created_on' : post.fecha
                    }
        rss.append(postrss)

    return dict(title="jennni's blog",
                link="http://maldonado.pl/blog/default/rss_blog.rss",
                description="Jenni's blog",
                entries  = rss )

def get():
    flick='Hola flickr!' 
    return dict(flick=flick)


