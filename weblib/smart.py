
from functools import wraps
from twisted.web import (server, resource, static,  html )



class Controller(resource.Resource):
    
    def render_GET(self, request):
        method = self.findRoute(request)
        return method(request) if method else "<html>404, unknown method</html>"
        
    def render_POST(self, request):
        method = self.findRoute(request)
        return method(request) if method else "<html>404, unknown method</html>"
        
    def findRoute(self, request):
        method = request.path.rsplit("/")[-1]
        if hasattr(self, "do_%s" % method):
            return getattr(self, "do_%s" % method)
        else:
            return None
        
    