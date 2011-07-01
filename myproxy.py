from middleman import Store
from twisted.web import proxy, http
from twisted.python.rebuild import Sensitive

class MyProxyClient(proxy.ProxyClient):
    myStore = Store()
    def __init__(self, command, rest, version, headers, data, father):
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)
        self.myStore.addHost(headers['host'], command, rest, headers, data)
        

 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient
    pass

class MyProxyRequest(proxy.ProxyRequest, Sensitive):
    protocols = {'http': MyProxyClientFactory}
    
 
class MyProxy(proxy.Proxy, Sensitive):
    """
    This class implements a simple web proxy.

    Since it inherits from L{twisted.protocols.http.HTTPChannel}, to use it you
    should do something like this::

        from twisted.web import http
        f = http.HTTPFactory()
        f.protocol = Proxy

    Make the HTTPFactory a listener on a port as per usual, and you have
    a fully-functioning web proxy!
    """

    requestFactory = MyProxyRequest
 
class ProxyFactory(http.HTTPFactory, Sensitive):
    protocol = MyProxy