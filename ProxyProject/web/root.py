



from txweb import expose
from static import relPath, ROOT, JS, CSS
from twisted.web.static import File


class Root(object):
    
    index = File(ROOT)
    css = File(CSS)
    js  = File(JS)
    
    