from twisted.web import proxy, http

class MyProxyClient(proxy.ProxyClient):
    pass
 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient
    pass

class MyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': MyProxyClientFactory}
    
 
class MyProxy(proxy.Proxy):
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
 
class ProxyFactory(http.HTTPFactory):
    protocol = MyProxy