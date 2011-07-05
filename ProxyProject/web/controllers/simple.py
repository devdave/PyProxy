from twisted.web.server import NOT_DONE_YET
from twisted.internet.defer import Deferred

from web.util.smart import (Controller, Must, Can )
from web.util.utilities import jsonify
from json import dumps
from data.store import Store


class Simple(Controller):
    myStore = Store()
    isLeaf = True
    
    @jsonify
    def process_host_count(self, request, params):
        try:
            data = self.myStore.getHostCount()
        except Exception, e:
            response = dict(success = False) 
        else:
            response = dict(success = True, ts = self.myStore.lastChange,  hosts = data)

        return response
        
    
    
    
    
    @Can(ts = float)
    def do_host_count(self, request, params = {}):
        """
            Because process_host_count above is meant to handle its
            own finalization, do_host_count always returns NOT_DONE_YET.  Its
            much simpler to make a tiny hack then hack process_host count to straddle
            to different scenarios ( return string and process itself )
        """
        
        #if this a polling request and it's not the first one
        if 'ts' in params and params['ts'] != 0:
            #if the caller is up to date or from the future
            if params['ts'] > self.myStore.lastChange:
                #hold the connection open
                d = Deferred()
                def deferred_host_count(self, request):
                    request.write(self.process_host_count)
                    request.finish()
                
                #and notify them when something changes
                d.addCallback(self.deferred_host_count, request)
                self.myStore.onChange.observe(d)
                return NOT_DONE_YET
                
       
        #If no TS or TS is out of date, process NOW
        
        return self.process_host_count(request)
        
                
        
        
        
            
        
        
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

    