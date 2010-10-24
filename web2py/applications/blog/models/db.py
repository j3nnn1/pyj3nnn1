# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    #db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    db = DAL('mysql://j3nnn1:j3nnn1@angvp.com/j3nnn1_blog') 
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:f3d5ade2-9740-497b-92a8-a0d5169de496'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################


db.define_table('usuarios',
        Field('usuario', 'string', requires= [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'usuarios.usuario')], required=True), 
        Field('clave', 'password', requires= [CRYPT(),IS_NOT_EMPTY()], required=True),
        Field('correo', 'string',  readable=False, writable=True, requires= [IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'usuarios.correo')], required=True))

import datetime
now = datetime.datetime.today()

db.define_table('articulos',
        Field('titulo',    'string',  requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'articulos.titulo')], required=True),
        Field('articulo',  'text',    requires=IS_NOT_EMPTY(),required=True),
        Field('fecha',     'datetime',default=now),
        Field('id_usuario',db.usuarios, readable=False, writable=False),
        Field('image', 'upload'))
        

db.define_table('comentarios',
        Field('id_articulo', db.articulos, readable=False, writable=False),
        Field('titulo',      'string',requires = IS_NOT_EMPTY(), required=True),
        Field('comentario',  'text',  requires = IS_NOT_EMPTY(), required=True),
        Field('nombre',      'string',requires = IS_NOT_EMPTY(), required=True),
        Field('correo',      'string',requires = [IS_EMAIL(), IS_NOT_EMPTY()],     required=True),
        Field('url',         'string',required=False),
        Field('fecha',       'datetime', default=now),
        Field('visible',     'boolean'))


db.define_table('etiquetas',
        Field('nombre', 'string', requires=IS_NOT_EMPTY(), required=True))
        

db.define_table('etiquetas_articulos', 
        Field('id_etiqueta',db.etiquetas, readable=False, writable=False),      
        Field('id_articulo',db.articulos, readable=False, writable=False))
