#Twisted
from twisted.web import (server, resource, static)
#Module specific
from os import mkdir
from os.path import (join, dirname, exists)
#app specific
from controllers.simple import Simple        
    
    
def GetSite(Config, store):
    """
        Puts it all together, building up the website
        @docRoot the base for the static file content
    """
    root = resource.Resource()
    root.putChild("", static.File(join(Config['web']['root'], "webapp", "index.html")))
    simple = Simple()
    simple.setStore(store)
    root.putChild("simple", simple )
    
    for element in Config['web']['elements']:
        root.putChild(element, static.File(join(Config['web']['root'], element)))    
    
    return server.Site(root)
    