



from txweb import expose
from static import relPath, ROOT, JS, CSS
from twisted.web.static import File
from twisted.python.rebuild import Sensitive
from twisted.web.server import NOT_DONE_YET
import render
from cgi import escape

from contextlib import contextmanager

from ProxyProject import data
from controllers.hosts import Hosts
from controllers.console import Console    


class Root(object, Sensitive):
    
    store = None
    
    def __init__(self, store):        
        data.bus.call("root.init", self)
    
    index = File(ROOT)
    css = File(CSS)
    js  = File(JS)
    
    
    hosts = Hosts()
    
    console = Console()