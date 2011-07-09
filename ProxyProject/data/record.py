
from StringIO import StringIO
from collections import defaultdict

class Record(object):
    """
        Wraps the process of recording both the request and response to a proxy request
    """


        
    def __init__(self):
        self.store = None
        self.request = dict(host = None, method = None, uri = None, header = None, args = None)
       
        #response
        self.response = dict(header = defaultdict(list), status = "-1", body = StringIO() )
        
    @property
    def host(self):
        self.request.get("host", None)
    
    @host.setter
    def host(self, value):
        self.request['host'] = value
    
    @property
    def uri(self):
    
    def addResponseHeader(name, value):
        self.response_headers[name].append(value)
        
    def setResponseHeader(name, value):
        self.response_headers[name] = value
        
    def writeResponse(self, raw):
        self.response_body.write(raw)
        
    def setStatus(self, status):
        self.response_status = status
        