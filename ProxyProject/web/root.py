



from txweb import expose
from static import relPath, ROOT, JS, CSS
from twisted.web.static import File
from twisted.python.rebuild import Sensitive
from twisted.web.server import NOT_DONE_YET
import render
from cgi import escape

from contextlib import contextmanager


from controllers.hosts import Hosts
        


class Root(object, Sensitive):
    
    store = None
    
    def __init__(self, store):
        self.store = store
        self.hosts.store = store
    
    index = File(ROOT)
    css = File(CSS)
    js  = File(JS)
    
    
    hosts = Hosts()
    
    