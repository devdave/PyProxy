from twisted.web import proxy, http
from twisted.python.rebuild import Sensitive

import urlparse

from ProxyProject.data.record import Record
from ProxyProject import data


"""
   Note:
   Twisted is a 2.4 legacy library that barely plays well with dbgp.
   Solution is to bind 
"""


class MyProxyClient(proxy.ProxyClient):
    """
        Override the default Proxy.ProxyClient
            Provides a hook for recording a proxy session at the midway
            point between twisted and the remote service
        
        Notes & todo's
            Either @ this level or one tier up at the Factory level
                place a post-response hook to allow for on the fly
                re-rendering of content/headers.
                
                One serious caveat is that the system correctly
                handles content-encoded like gzip or deflate.  A dirt
                simple solution would be to find and remove the request
                header saying it would accept compressed content.
                
                Second problem is chunked content.  That could be resolved
                by buffering incoming content no matter what, and simply
                stripping the response header                
        
    """
    def __init__(self, command, rest, version, headers, argdata, father):
        """
            command := HTTP method ( GET | POST | HEAD )
            rest    := HTTP uri
            version := ex 1.1
            headers := Request headers
            data    := A query string regardless of method
            father  := ??? Still unknown
        """
        
        #Well known bug that was resolved... yet sometimes squeeks through to this point
        #proxy-con would hang twisted if not resolved
        if "proxy-connection" in headers:
            del headers["proxy-connection"]
        
        #Explicitly tell the server this is a 1 time deal, no pipelining
        headers["connection"] = "close"
        headers.pop('keep-alive', None)          
        proxy.ProxyClient.__init__(self, command, rest, version, headers, argdata, father)
        
        data.bus.call("proxy-client.init", self)      
        #Delegated task of collection to Record__init__
        
        
    
    def handleStatus(self, version, code, message):        
        proxy.ProxyClient.handleStatus(self,version,code, message)        
        self.pxRecord.setStatus(code, message)
    
    def handleHeader(self, key, value):
        # Simple Out of band communication
        # the tail of this key becomes the key in Record.oob
        if key.startswith('x-devprox-'):
            self.pxRecord.oob[key[len('x-devprox-'):]] = value
            return
                
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
            
            Notes: lineage failures are almost always
            directly attributed to server timesouts.  Somewhere on the
            internet is a major public service that hates me.
        """
        
            
        try:
            data.bus.call("proxy-client.handleResponseEnd", self )
        except Exception as e:
            print "Unhandled exception due to data.bus call proxy-client.handleResponseEnd ", e
            
        if not self._finished:
            self._finished = True
            self.father.finish()
            self.transport.loseConnection()
        
class MyProxyClientFactory(proxy.ProxyClientFactory, object):
    protocol = MyProxyClient

class MyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': MyProxyClientFactory}
    
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        host = parsed[1]
        if protocol not in self.ports:
            #TODO most liekly this is google attempting a CONNECT
            #tunnel.
            raise Exception("Invalid request %s : %s " % ( self.method, self.uri) )
            
        port = self.ports.get(protocol, 80)
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        rest = urlparse.urlunparse(('', '') + parsed[2:])
        if not rest:
            rest = rest + '/'
        if protocol not in self.protocols:
            debug = 1
            debug = 2
            
        class_ = self.protocols.get(protocol, "http")
        headers = self.getAllHeaders().copy()
        if 'host' not in headers:
            headers['host'] = host
        self.content.seek(0, 0)
        s = self.content.read()
        
        
        data.bus.call("ProxyRequest.process", self)
        clientFactory = class_(self.method, rest, self.clientproto, headers,
                               s, self)
        #todo use the AbortException here to allow for replay calls    
        self.reactor.connectTCP(host, port, clientFactory)    
    
class MyProxy(proxy.Proxy):
    requestFactory = MyProxyRequest
    
class ProxyFactory(http.HTTPFactory):
    protocol = MyProxy
    
    