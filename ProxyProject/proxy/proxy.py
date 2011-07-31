from twisted.web import proxy, http
from twisted.python.rebuild import Sensitive

from data.record import Record
import data.bus

class MyProxyClient(proxy.ProxyClient):
    
    def __init__(self, command, rest, version, headers, data, father):
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)
        # @todo I can use a setter as I depend on grabbing request @ instantiation
        # but the journey below seems fragile
        self.pxRecord = Record(self)
        
    
    def handleStatus(self, version, code, message):
        proxy.ProxyClient.handleStatus(self,version,code, message)        
        self.pxRecord.setStatus(code, message)
    
    def handleHeader(self, key, value):
        # t.web.server.Request sets default values for these headers in its
        # 'process' method. When these headers are received from the remote
        # server, they ought to override the defaults, rather than append to
        # them.
        if key.lower() in ['server', 'date', 'content-type']:
            self.father.responseHeaders.setRawHeaders(key, [value])
            self.pxRecord.setResponseHeader(key, value)
        else:
            self.father.responseHeaders.addRawHeader(key, value)
            self.pxRecord.addResponseHeader(key, value)
            
    def handleResponsePart(self, buffer):
        proxy.ProxyClient.handleResponsePart(self, buffer)        
        self.pxRecord.writeResponse(buffer)
    
    def handleResponseEnd(self):
        """
            Haven't traced it out yet but ocassionally father is missing channel or
            factory... which shouldn't be possible?
        """
        data.bus.first("data.store.addRecord", self.pxRecord )
        
        if not self._finished:
            self._finished = True
            self.father.finish()
            self.transport.loseConnection()
        
    
        
    
 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient

class MyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': MyProxyClientFactory}
    
 
class MyProxy(proxy.Proxy):
    requestFactory = MyProxyRequest
    
 
class ProxyFactory(http.HTTPFactory):
    protocol = MyProxy
    
    