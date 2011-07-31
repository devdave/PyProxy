
from StringIO import StringIO
from collections import defaultdict

class Record(object):
    """
        Wraps the process of recording both the request and response to a proxy request
    """


        
    def __init__(self, client):        
        self.request = dict(host = client.headers.get("host", "Runtime error!"), method = client.command, uri = client.rest, headers = client.headers, data = client.data)
        #response
        self.response = dict(headers = defaultdict(list), status = "-1", body = StringIO() )
        
    def addResponseHeader(self, name, value):
        self.response['headers'][name].append(value)
        
    def setResponseHeader(self, name, value):
        self.response['headers'][name] = value        
        
    def writeResponse(self, raw):
        self.response['body'].write(raw)        
        
    def setStatus(self, code, message):
        self.response['status'] = dict(code = code, message = message )
        
    def raw(self):
        return dict(response = self.response, request = self.request )