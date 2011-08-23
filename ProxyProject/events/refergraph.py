
"""
    Hooks in at the uri page 
"""
from txweb.util import expose
from ProxyProject import data

class RefererGraph(object):
    
    @expose
    def index(self, request):
        return "Hello World!"
    
    
    
def onRootInit(root):
    root.graph = RefererGraph()
    

def initialize():
    data.bus.register("web.root.init", onRootInit)
    