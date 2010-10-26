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
                  
    page = int(request.vars.page) if request.vars.page else 1
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
        filtro      = ((db.articulos.id==request.args(0)) & (db.articulos.id_usuario==db.auth_user.id))
        post        = db(filtro).select(db.articulos.ALL, db.auth_user.first_name).first()

        if post:
            form        = SQLFORM(db.comentarios)
            form.vars.id_articulo = post.articulos.id
            filtro          = ((db.comentarios.id_articulo==post.articulos.id)&(db.comentarios.visible=='1'))
            comments        = (db(filtro).select(db.comentarios.ALL, orderby=~db.comentarios.fecha)).records 
	    #print db._lastsql
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
    
    tableart = db().select(db.articulos.ALL, orderby=~db.articulos.fecha).records

    return dict(tableart=tableart)


@auth.requires_login()
def modifypost():

    if request.args(0):  #modificando un post

        post   = db.articulos(request.args(0)) or redirect(URL('index'))
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

    form        = SQLFORM(db.articulos)
    form.vars.id_usuario = auth.user.id

    if form.accepts(request.vars, session):
        response.flash ='Tu articulo ha sido publicado'

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
