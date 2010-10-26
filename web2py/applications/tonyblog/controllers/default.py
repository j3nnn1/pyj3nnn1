import os
from gluon.contenttype import contenttype
from gluon.fileutils import check_credentials
    
record=db(db.pagename.id == 1).select()[0]
person = record.title  

admin = True
               
###########################################################
### main index
############################################################

def index(): 
    person = "Blog user"
    rows = db().select(db.image.ALL)
    
    try:
        if check_credentials(request): admin = True
    except:
        admin = False

    return dict(images = rows, admin = admin, person = person) 
    

###########################################################
### show a record
############################################################

    
def show():
    id = int(request.args[0])
    row = db(db.image.id == id).select()[0]  
    myform = SQLFORM(db.comment, fields = ['author', 'email', 'body'])
    myform.vars.image_id = id;
    if myform.accepts(request.vars,session):  response.flash = "comment posted" 
    
    try:
        if check_credentials(request): admin = True 
    except:
        admin = False 
        

    comments = db(db.comment.image_id == id).select()
    return dict(image = row, comments = comments, myform = myform, admin = admin, person = person)
    

###########################################################
### download file
############################################################

    
def download():
    filename=request.args[0]
    response.headers['Content-Type']=contenttype(filename)
    return open(os.path.join(request.folder,'uploads/','%s' % filename),'rb').read()
    


###########################################################
### insert a new record
############################################################


def insert():
    if not admin: redirect(URL(r=request,f='index'))
    form=SQLFORM(db.image)
    if form.accepts(request.vars,session): response.flash='new record inserted'
    return dict(form=form, person = person)
    

###########################################################
### edit delete one record
############################################################

def update():
    if not admin: redirect(URL(r=request,f='index'))
    id=int(request.args[0])
    record=db(db.image.id==id).select()[0]
    form=SQLFORM(db.image,record,deletable=True)
                 #upload=URL(r=request,f='download/'))
    if form.accepts(request.vars,session): 
        response.flash='done!'        
        redirect(URL(r=request,f='index'))
    return dict(form=form, person = person)
    
##########################################################
### edit title
############################################################

def title():
    if not admin: redirect(URL(r=request,f='index'))
    id=int(request.args[0])
    record=db(db.pagename.id == 1).select()[0]
    form=SQLFORM(db.pagename, record, deletable=False)
    if form.accepts(request.vars,session): 
        response.flash='done!'   
        redirect(URL(r=request,f='index')) 
         
    return dict(form = form, person = person)