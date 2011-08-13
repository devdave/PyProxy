from collections import (defaultdict)
from time import time

from twisted.internet import defer

#from util.singleton import Singleton
from util.observable import Observable
from data.record import Record

        
class Store(object):
    
    def __init__(self):
        self.lastChange = time()
        self.data = defaultdict( lambda : defaultdict(list) )
        self.hostCount = defaultdict(int)
        self.onChange = Observable()
        
        
    def addChangeObserver(self):
        self.onChange(self.doOnChange)
        
        
    def doOnChange(self, *args, **kwargs):
        self.lastChange = time()
        self.addChangeObserver()
    
        
    def addRecord(self, record):
        """
            host - A non-empty string that is the FQDN of a web host
            method - Should be POST or GET, but can also be PUT, DELETE, or CONNECT
            uri - A non-empty string that is the uri for the request
            headers - a dictionary of the requests headers
            ext - Preferablly a dictionary of GET or POST arguments
        """
        host = record.request['host']
        self.hostCount[host] += 1
                
        #Can't believe this works :0
        self.data[host][record.request['uri']].append( record )
        
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
        uris    = self.data[host].keys()
        return dict(host = host, uris = uris, ts = self.lastChange )
        
    def getTRXByHostURI(self, host, uri):
        return self.data[host][uri]
        