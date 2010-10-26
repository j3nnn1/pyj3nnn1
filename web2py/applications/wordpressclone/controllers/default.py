from gluon.fileutils import check_credentials
session.authorized=check_credentials(request)

response.title = "PyPress - a web2py powered weblog"
response.keywords = "web2py, Gluon, Python, Enterprise, Web, Framework, PyPress"
response.description = "Just another PyPress weblog"

# This dynamically adds the pages to the menu
pages = db(db.posts.post_type == 'page').select(db.posts.ALL)
items = []
for page in pages:
    item = [page.post_title, False, '/%(app)s/default/page/%(id)s' % {'app':request.application, 'id':page.id}]
    items.append(item)
response.menu = items

# This returns all the categories and their post count
cats = db().select(db.categories.ALL)
items = []
for cat in cats:
    count = len(db(
                   (db.posts.post_type == 'post') & 
                   (db.posts.post_category == cat.id)
                   ).select(db.posts.ALL))
    if count > 0:
        item = [cat.category_name, count, '/%(app)s/default/category/%(name)s' % {'app':request.application, 'name':cat.category_name}]
        items.append(item)
response.categories = items

# This returns all the links
links = db().select(db.links.ALL)
items = []
for link in links:
    item = [link.link_title, link.link_url, link.id]
    items.append(item)
response.links = items

# The main page
# Shows the first 10 posts    
def index():
    posts = db(db.posts.post_type == 'post').select(db.posts.ALL, orderby=~db.posts.post_time)
    return dict(posts = posts)

# The post page
# Shows the entire post, the comments, and the comment form
def post():
    #try: 
    post_id = int(request.args[0])
    post = db(db.posts.id == post_id).select()[0]
    comments = db(db.comments.post_id == post_id).select(db.comments.ALL)
    comment_count = len(db(db.comments.post_id == post_id).select(db.comments.ALL))
    db.comments.post_id.default = post_id
    comment_form = SQLFORM(db.comments, fields = ['comment_author', 'comment_author_email', 'comment_author_website', 'comment_text'], labels = comment_labels)
        
    if comment_form.accepts(request.vars, session):
        session.flash = "Comment added."
        redirect(URL(r = request,f = 'index'))
        
    return dict(post = post, comments = comments, comment_form = comment_form, comment_count = comment_count)
    #except: 
    #    redirect(URL(r = request,f = 'index'))

# The page page
# Shows the entire page. Does not show comments or the comment form
def page():
    try: 
        post_id = int(request.args[0])
        post = db(db.posts.id == post_id).select()[0]
        return dict(post = post)
    except: 
        redirect(URL(r = request,f = 'index'))

# The category page
# Shows all the posts in the requested category
def category():
    try:
        cat_name = request.args[0]
        posts = db(
                   (db.posts.post_type == 'post') &
                   (db.posts.post_category == db.categories.id) &
                   (db.categories.category_name == cat_name)
                   ).select(db.posts.ALL, orderby=~db.posts.post_time)
        response.sidebar_note = "You are currently browsing the archives for the %s category." % cat_name
        return dict(posts = posts)
    except:
        redirect(URL(r = request,f = 'index'))

def add():
    try:
        area = request.args[0]

        if area == "post":
            db.posts.post_type.default = 'post'
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text', 'post_category'], labels = post_labels)
            page_title = "Add Post"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Post added."
                redirect(URL(r = request,f = 'index'))
        
        elif area == "page":
            db.posts.post_type.default = 'page'
            page_form = SQLFORM(db.posts, fields = ['post_title', 'post_text'], labels = post_labels)
            page_title = "Add Page"
            
            if page_form.accepts(request.vars, session):
                session.flash = "Page added."
                redirect(URL(r = request,f = 'index'))
                
        else:
            redirect(URL(r = request,f = 'index'))
            
        return dict(page_title = page_title, page_form = page_form)
    except:
        redirect(URL(r = request,f = 'index'))

def edit():

    try:
        area = request.args[0]
        id = request.args[1]
    except:
        redirect(URL(r = request,f = 'index'))
    
    if area == 'post':
        this_item = db(db.posts.id == id).select()[0]
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text', 'post_category'], labels = post_labels)
        edit_title = "Edit Post"
    
        if edit_form.accepts(request.vars, session):
            session.flash = "Post updated."
            redirect(URL(r = request,f = 'post/%s' %id))

    elif area == 'page':
        this_item = db(db.posts.id == id).select()[0]
        edit_form = SQLFORM(db.posts, this_item, fields = ['post_title', 'post_text'], labels = post_labels)
        edit_title = "Edit Page"
    
        if edit_form.accepts(request.vars, session):
            session.flash = "Page updated."
            redirect(URL(r = request,f = 'page/%s' %id))
                    
    else:
        redirect(URL(r = request,f = 'index'))
    
    return dict(edit_form = edit_form, edit_title = edit_title)

        
def manage():

    area = request.args[0]
    
    try: command = request.args[1]
    except: command = ""
        
    if area == 'link':
        rows = db().select(db.links.ALL)
        manage_title = 'Manage Links'

        if command == 'add':
            edit_form = SQLFORM(db.links, labels = link_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = "Link added"
                redirect(URL(r = request, f = 'manage/link'))
            else:
                session.flash = "Error"
       
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_link = db(db.links.id == id).select()[0]
                edit_form = SQLFORM(db.links, this_link)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = "Link updated"
                    redirect(URL(r = request, f = 'manage/link'))
                else:
                    session.flash = "Error"
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.links.id == id).delete()
                session.flash = "Link deleted"
                redirect(URL(r = request, f = 'manage/link'))
    
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)
    
    elif area == 'category':
        rows = db().select(db.categories.ALL)
        manage_title = 'Manage Categories'
       
        if command == 'add':
            edit_form = SQLFORM(db.categories, labels = cat_labels)
            
            if edit_form.accepts(request.vars, session):
                session.flash = "Category added"
                redirect(URL(r = request, f = 'manage/category'))
            else:
                session.flash = "Error"
        
        elif command == 'edit':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                this_cat = db(db.categories.id == id).select()[0]
                edit_form = SQLFORM(db.categories, this_cat)
                
                if edit_form.accepts(request.vars, session):
                    session.flash = "Category updated"
                    redirect(URL(r = request, f = 'manage/category'))
                else:
                    session.flash = "Error"
        
        elif command == 'delete':
            try: id = request.args[2]
            except: id = ""
            
            if id != '':
                db(db.categories.id == id).delete()
                session.flash = "Category deleted"
                redirect(URL(r = request, f = 'manage/category'))
        
        else:
            edit_form = ''
            
        return dict(rows = rows, manage_title = manage_title, edit_form = edit_form, area = area)        
    
    else:
        redirect(URL(r = request,f = 'index'))