

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import NOT_DONE_YET
import sys
log.startLogging(sys.stdout)



from ProxyProject.proxy.proxy import ProxyFactory

from ProxyProject import data
from ProxyProject import events
from ProxyProject import web
from ProxyProject import data
from ProxyProject.config import Config



from os.path import (dirname, abspath, join)


from twisted.internet.task import LoopingCall


    

if __name__ == '__main__':
    
    
    
    data.initialize()
    events.initialize()
    store = data.bus.must("data.store")
    reactor.listenTCP(Config['web']['port'], web.buildSite( store ) )
    reactor.listenTCP(Config['proxy']['port'], ProxyFactory())    
    
    reactor.run()