# try something like
db=SQLDB("sqlite://db.db")

db.define_table('image',
    SQLField('title'),
    SQLField('file','upload'), 
    SQLField('body','text')) 
    
db.define_table('comment', 
    SQLField('author'),
    SQLField('email'),
    SQLField('body', 'text'),
    SQLField('image_id',db.image))
    
db.define_table('pagename',
    SQLField('title', default = "Blog user"))