from twisted.web import proxy, http
from twisted.python.rebuild import Sensitive

#from data.store import Store

class MyProxyClient(proxy.ProxyClient):
    
    def __init__(self, command, rest, version, headers, data, father):
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)
        # @todo I can use a setter as I depend on grabbing request @ instantiation
        # but the journey below seems fragile
        self.pxRecord = father.channel.factory.myStore.newRecord()
        self.pxRecord.host = header['host']
        self.pxRecord.uri = rest
        self.pxRecord.method = command
        self.pxRecord.
        self.myStore.addRequest(headers['host'], command, rest, headers, data)
        

 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient

class MyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': MyProxyClientFactory}
    
 
class MyProxy(proxy.Proxy):
    requestFactory = MyProxyRequest
    
 
class ProxyFactory(http.HTTPFactory):
    protocol = MyProxy
    
    def __init__(self, *args, **kwargs):
        self.myStore = None
        http.HTTPFactory.__init__(self, *args, **kwargs)
        
    def setStore(self, store):
        self.myStore = store