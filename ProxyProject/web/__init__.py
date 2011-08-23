"""
    Root of Web, intra-package/module access should funnel through here
"""
#plugins
from txweb import Site
#app
from root import Root

from ProxyProject import data


from ProxyProject.modulereloader import ModuleReloader


class Oversite(Site):
    def __init__(self, store, *args, **kwargs):
        Site.__init__(self, *args, **kwargs)
        self.store = data.bus.must("data.store")
        
    def prefilter(self, request, resource):
        request.store = self.store        
        
        


def buildSite(store):
    return Oversite(store, Root(store))    
    
    

reloader = ModuleReloader.WatchThis(__file__)