
from StringIO import StringIO
from collections import defaultdict
import zlib

import pickle
from time import time

class Record(object):
    """
        Wraps the process of recording both the request and response to a proxy request
    """

    def __init__(self, client):        
        self.request = dict(host = client.headers.get("host", "Runtime error!"), method = client.command, uri = client.rest, headers = client.headers, data = client.data)
        #response
        self.response = dict(headers = defaultdict(list), status = "-1", body = "" )
        #out of band data like headers starting with "x-devprox-" or the request timers below
        self.oob = dict()
        self.oob['created'] = time()
        self.oob['finished'] = -1
        
        self._id = id(self.request)
    
    
    @property
    def id(self):
        return self._id
        
    def isFinished(self):
        self.finished = time()
    
    @property
    def runTime(self):
        return max([0, self.oob['finished'] - self.oob['created'] ] )
    
    @property
    def host(self):
        return self.request['host']
    
    @property
    def uri(self):
        return self.request['uri']
        
        
    def addResponseHeader(self, name, value):
        self.response['headers'][name].append(value)
        
    def setResponseHeader(self, name, value):
        self.response['headers'][name] = value        
        
    def writeResponse(self, raw):
        self.response['body'] += raw
        
    def setStatus(self, code, message):
        self.response['status'] = dict(code = code, message = message )
        
    def raw(self):
        return dict(response = self.response, request = self.request )
        
    def getBody(self):
        body = body = self.response['body']
        if 'Content-Encoding' in self.response['headers'] and 'gzip' in self.response['headers']['Content-Encoding']:            
            body = zlib.decompress(StringIO(body), 16+zlib.MAX_WBITS)
            
        return body
        
    def __eq__(self, other):
        """
            Compares two records for equality, with the exception of the Date field which should
            always be different, but is illrelevant to equality testing
        """
        selfResponse = dict( self.response.items())
        otherResponse = dict( other.response.items())
        
        del selfResponse['headers']['Date']
        del otherResponse['headers']['Date']
        
        try:
            return self.request == other.request and selfResponse == otherResponse
        finally:            
            del selfResponse
            del otherResponse
    
    def __getstate__(self):
        return dict(request = self.request, response = self.response, oob = self.oob )
        
    def __setstate(self, state):
        #If for some reason a record is pulled back up and it's not complete, buy some time to allow for inspection from console
        deserializationFailure = lambda : "Deserialization failure"
        
        self.request    = state.get('request', deserializationFailure)
        self.response   = state.get("response", deserializationFailure)
        self.oob        = state.get("oob", deserializationFailure )
        self._id = id(self.request)