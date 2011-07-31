

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
    Config['web']["root"] = join(abspath(dirname(__file__)) , Config['web']["root"] )
    
    store = Store()
    data.bus.register("data.store.addRecord", store.addRecord )
    
    #I swear to god, the names are all entirely accidental
    reactor.listenTCP(Config['web']['port'], web.site )
    reactor.listenTCP(Config['proxy']['port'], ProxyFactory())    
    
    reactor.run()