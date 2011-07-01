from collections import (defaultdict, namedtuple)
"""
   Store is an abomination of all that is holy in sane software development
   BUT, it works and is a heck of a lot simpler then the other idea's I had
   
"""

RequestRecord = namedtuple("RequestRecord", "host,uri,method,headers,args")


class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Store(Singleton):
    
    def __init__(self):
        self.data = dict()
        self.hostCount = defaultdict(int)
        
        
    def addHost(self, host, method = "UNK", uri = "/", headers = {}, ext = None):
    
        self.hostCount[host] += 1
        if host not in self.data:
            self.data[host] = dict()
        
        if uri not in self.data[host]:
            self.data[host][uri] = []
        
        #Can't believe this works :0
        self.data[host][uri].append( dict(host = host, uri = uri, method = method, headers = headers, ext = ext))
        
            
            
        
    
    def ClearHost(cls, host):
        if host in self.data:
            del self.data[host]
        
        return true
    
    def getHostCount(self):
        data = []
        for name, value in self.hostCount.items():        
            data.append(dict(host = name, count = value ))
        return data