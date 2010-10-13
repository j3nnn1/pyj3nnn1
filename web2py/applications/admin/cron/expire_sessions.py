EXPIRATION_MINUTES=60
import os, time, stat, logging
path=os.path.join(request.folder,'sessions')
if not os.path.exists(path):
   os.mkdir(path)
now=time.time()
for file in os.listdir(path):
   filename=os.path.join(path,file)
   try:
      t=os.stat(filename)[stat.ST_MTIME]
      if os.path.isfile(filename) and now-t>EXPIRATION_MINUTES*60 \
             and file.startswith(('1','2','3','4','5','6','7','8','9')):
         try:
            os.unlink(filename)
         except Exception,e:
            logging.warn('failure to unlink %s: %s' % (filename,e))
   except Exception, e:
      logging.warn('failure to stat %s: %s' % (filename,e))
         
