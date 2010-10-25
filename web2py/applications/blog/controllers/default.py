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
    filtro = (db.articulos.id_usuario==db.usuarios.id)
    perpage = 3                                  # Numero de articulos por pagina
    totalposts = db(db.articulos.id > 0).count() # contamos cuantos posts hay en la bd
    totalpages = totalposts / perpage            # division para sacar el numero de paginas
                  
    page = int(request.vars.page) if request.vars.page else 1
    limit = int(page - 1) * perpage
                         
    if totalposts > perpage and totalpages == 1 and totalpages * perpage != totalposts:
        totalpages = 2
                                                        
    post = db(filtro).select(db.articulos.ALL, db.usuarios.usuario,limitby=(limit,page*perpage),orderby=~db.articulos.fecha)

    return dict(post=post,totalpages=totalpages,postpage=page)

def about():
    """ Información sobre mi persona"""
    return dict()

def viewpost():
    if request.args(0):
        filtro      = ((db.articulos.id==request.args(0)) & (db.articulos.id_usuario==db.usuarios.id))
        post        = db(filtro).select(db.articulos.ALL, db.usuarios.usuario).first()

        if post:
            form        = SQLFORM(db.comentarios)
            form.vars.id_articulo = post.articulos.id
            filtro          = (db.comentarios.id_articulo==post.articulos.id)
            comments        = (db(filtro).select(db.comentarios.ALL, orderby=~db.comentarios.fecha)).records 
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
