from twisted.web.server import NOT_DONE_YET
from twisted.internet.defer import Deferred

from web.util.smart import (Controller )
from web.util.utilities import jsonify
from json import dumps
from data.store import Store


class Simple(Controller):
    myStore = Store()
    isLeaf = True
    
    
    def process_host_count(self, request):
        try:
            data = self.myStore.getHostCount()
        except Exception, e:
            response = dict(success = False) 
        else:
            response = dict(success = True, ts = self.myStore.lastChange,  hosts = data)

        request.write(dumps(response))
        request.finish();
        return
        
    

    def do_host_count(self, request):
        """
            Because process_host_count above is meant to handle its
            own finalization, do_host_count always returns NOT_DONE_YET.  Its
            much simpler to make a tiny hack then hack process_host count to straddle
            to different scenarios ( return string and process itself )
        """
        
        #if this a polling request and it's not the first one
        if 'ts' in request.args and request.args['ts'][0] != '0':
            #if the caller is up to date or from the future
            if float(request.args['ts'][0]) >= self.myStore.lastChange:
                #hold the connection open
                d = Deferred()
                #and notify them when something changes
                d.addCallback(self.process_host_count, request)
                self.myStore.onChange.observe(d)
                return NOT_DONE_YET
                
       
        #If no TS or TS is out of date, process NOW
        self.process_host_count(request)
        return NOT_DONE_YET
        
                
        
        
        
            
        
        
    @jsonify    
    def do_describe(self, request):
        host = request.args.get('host', [""])[0]
        return self.myStore.data.get(host, None)        
    
    @jsonify    
    def do_digest(self, request):
        host = request.args.get('host', [""])[0]
        uri = request.args.get("uri", [""])[0]
        hostURIs = self.myStore.data.get(host, None)
        data = hostURIs[uri] if hostURIs else None        
        return data

    