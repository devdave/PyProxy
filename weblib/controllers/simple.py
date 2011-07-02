
from weblib.smart import (Controller )
from weblib.utilities import jsonify
from middleman import Store


class Simple(Controller):
    myStore = Store()
    isLeaf = True
    
    @jsonify
    def do_host_count(self, request):
        
        try:
            data = self.myStore.getHostCount()
        except Exception, e:
            return dict(success = False)
        else:
            return dict(success = True, hosts = data)
            
        
        
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

    