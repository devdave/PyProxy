

from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)

#Pun wasn't intended
from web.site import GetSite
from proxy.proxy import ProxyFactory
from data.store import Store

from os.path import (dirname, abspath, join)
from config import Config


if __name__ == '__main__':
    Config['web']["root"] = join(abspath(dirname(__file__)) , Config['web']["root"] )
    
    store = Store()
        
    reactor.listenTCP(Config['web']['port'], GetSite(Config, store))
    px = ProxyFactory()
    px.setStore(store)
    
    reactor.listenTCP(Config['proxy']['port'], px)
    reactor.run()