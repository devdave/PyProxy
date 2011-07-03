from twisted.web import proxy, http
from twisted.python.rebuild import Sensitive

from data.store import Store

class MyProxyClient(proxy.ProxyClient):
    myStore = Store()
    def __init__(self, command, rest, version, headers, data, father):
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)
        #start watching for response here or higher up?
        self.myStore.addRequest(headers['host'], command, rest, headers, data)
        

 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient

class MyProxyRequest(proxy.ProxyRequest, Sensitive):
    protocols = {'http': MyProxyClientFactory}
    
 
class MyProxy(proxy.Proxy, Sensitive):
    requestFactory = MyProxyRequest
 
class ProxyFactory(http.HTTPFactory, Sensitive):
    protocol = MyProxy