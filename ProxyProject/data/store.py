from collections import (defaultdict)
from time import time
import pickle

from twisted.internet import defer

#from util.singleton import Singleton
from util.observable import Observable
from record import Record

def internalDataDict():
    """
        Pickle doesnt like lambda's, so this is a work around
    """
    return defaultdict(list)
        
class Store(object):
    instanceCount = 0
    
    def __init__(self, data = None, lastChange = None, recordIndex = None, hostCount = None):
        self.instanceCount+= 1
        if self.instanceCount > 1:
            #Bad idea, should be a warning
            raise Exception("PANIC, there can only be one instance of data.Store")
    
        self.lastChange = time()
        self.data = data or defaultdict( internalDataDict ) 
        self.hostCount = defaultdict(int)
        self.recordIndex = {}
        self.onChange = Observable()
        #data storage space for plugins & extensions
        self.plugins = {}
        
    def addChangeObserver(self):
        self.onChange(self.doOnChange)
        
        
    def doOnChange(self, *args, **kwargs):
        self.lastChange = time()
        self.addChangeObserver()
        #Alternative callback
        data.bus.call("data.store.doOnChange")
    
    def map2uri(self, host, uri, mapper):
        """
            Applies the function mapper to every record for a specific
            uri.
        """
        data = []
        if host in self.data and uri in self.data[host]:
            data = [mapper(record) for record in self.data[host][uri]]        
        return data
    
    def addRecord(self, record):
        """
            host - A non-empty string that is the FQDN of a web host
            method - Should be POST or GET, but can also be PUT, DELETE, or CONNECT
            uri - A non-empty string that is the uri for the request
            headers - a dictionary of the requests headers
            ext - Preferablly a dictionary of GET or POST arguments
        """
        record.isFinished()
        
        host = record.request['host']
        uri  = record.request['uri']        
        self.hostCount[host] += 1
        isNew = False
        
        if host in self.data and uri in self.data[host] and len( self.data[host][uri]) > 0:            
            #Avoid duplicates
            for oldRecord in self.data[host][uri]:
                if oldRecord == record:
                    isNew = False
                    break
            else:
                isNew = True
        else:
            isNew = True
            
        if isNew:
            self.data[host][uri].append( record )
            self.recordIndex[hash(record)] = record
            
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
    
    def getRecordById(self, r_id):
        try:
            return self.recordIndex.get(int(r_id), None)
        except ValueError:
            return None
    
    @classmethod
    def saveTo(cls, inst, filepath, overwrite = False):
        with open(filepath, "wb") as myFile:
            return pickle.dump(inst, myFile)
    
    @classmethod
    def readFrom(cls, filepath):
        with open(filepath, "rb") as myFile:
            return pickle.load(myFile)
        
    
    
    def __getstate__(self):
        return dict(data = self.data)

    def __getinitargs__(self):
        """
            To cutdown on cruft, tell Pickle to call __init__ with no
            arguments
        """
        return ("data")
            
    def __setstate__(self, state):
        """
            TODO getinitargs doesn't seem to be working correctly
        """
        self.data = state['data']
        self.hostCount = defaultdict(int)
        self.recordIndex = {}
        
        for host in self.data.keys():            
            for record in self.data[host]:
                self.hostCount[host] += 1
                self.recordIndex[record.id] = record
        
        self.lastChange = time()        
        self.onChange = Observable()