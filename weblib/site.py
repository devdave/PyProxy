#Twisted
from twisted.web import (server, resource, static)
#Module specific
from os import mkdir
from os.path import (join, dirname, exists)
#app specific
from controllers.simple import Simple        
    
    
def GetSite(Config):
    """
        Puts it all together, building up the website
        @docRoot the base for the static file content
    """
    root = resource.Resource()
    #root.putChild("", static.File(join(Config['web']['root'], "webapp")))
    root.putChild("simple", Simple())
    
    for element in Config['web']['elements']:
        #exists to evaluate wit dbgp for correctnesss, todo exists check as well
        debugPath = join(Config['web']['root'], element)        
        if not exists(debugPath):
            mkdir(debugPath)        
        root.putChild(element, static.File(debugPath))    
    
    return server.Site(root)
    