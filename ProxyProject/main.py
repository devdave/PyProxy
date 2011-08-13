

from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)



from proxy.proxy import ProxyFactory
from data.store import Store
import web

import data.bus

from os.path import (dirname, abspath, join)
from config import Config


    

if __name__ == '__main__':
    
    store = Store()
    data.bus.register("data.store.addRecord", store.addRecord )
    #Hack to ensure Store instance is accessible elsewhere
    data.bus.register("data.store", lambda : store )
    
    #I swear to god, the names are all entirely accidental
    reactor.listenTCP(Config['web']['port'], web.buildSite(store) )
    reactor.listenTCP(Config['proxy']['port'], ProxyFactory())    
    
    reactor.run()