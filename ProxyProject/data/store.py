from collections import (defaultdict)
from time import time

from twisted.internet import defer

from util.singleton import Singleton
from util.observable import Observable

        
class Store(Singleton):
    """
        Store is an abomination of all that is holy in sane software development
        BUT, it works and is a heck of a lot simpler then the other idea's I had   
    """
    
    def __init__(self):
        self.lastChange = time()
        self.data = dict()
        self.hostCount = defaultdict(int)
        self.onChange = Observable()
        
        self.addChangeObserver()
        
    def addChangeObserver(self):
        d = defer.Deferred()
        d.addCallback(self.doOnChange)
        self.onChange.observe( d )
        
    def doOnChange(self, *args, **kwargs):
        self.lastChange = time()
        self.addChangeObserver()
    
        
    def addRequest(self, host, method = "UNK", uri = "/", headers = {}, ext = None):
        """
            host - A non-empty string that is the FQDN of a web host
            method - Should be POST or GET, but can also be PUT, DELETE, or CONNECT
            uri - A non-empty string that is the uri for the request
            headers - a dictionary of the requests headers
            ext - Preferablly a dictionary of GET or POST arguments
        """
        self.hostCount[host] += 1
        if host not in self.data:
            self.data[host] = dict()
        
        if uri not in self.data[host]:
            self.data[host][uri] = []
        
        #Can't believe this works :0
        self.data[host][uri].append( dict(host = host, uri = uri, method = method, headers = headers, ext = ext))
        
        #Tell anything who cares that things have changed
        self.onChange.emit(True)    
            
            
        
    
    def clearHost(self, host):
        if host in self.data:
            del self.data[host]
        if host in self.hostCount:
            del self.hostCount[host]            
        self.onChange.emit(True)
        return True
    
    def getHostCount(self):
        data = []
        for name, value in self.hostCount.items():        
            data.append(dict(host = name, count = value ))
        return data
        
    def getURISByHost(self, host):
        raise Exception("Todo")