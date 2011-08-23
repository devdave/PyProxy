

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import NOT_DONE_YET
import sys
log.startLogging(sys.stdout)



from proxy.proxy import ProxyFactory

import data.bus
import events
import web
import data




from os.path import (dirname, abspath, join)
from config import Config

from twisted.internet.task import LoopingCall


    

if __name__ == '__main__':
    
    
    
    data.initialize()
    events.initialize()
    store = data.bus.must("data.store")
    reactor.listenTCP(Config['web']['port'], web.buildSite( store ) )
    reactor.listenTCP(Config['proxy']['port'], ProxyFactory())    
    
    reactor.run()