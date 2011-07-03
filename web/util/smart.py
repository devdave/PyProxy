

from functools import wraps
from twisted.web import (server, resource, static,  html )

class RequestTypes:
    POST = 1<<1
    GET  = 1<<2
    ANY  = 1<<3
    

    
class Must(object):
    """
        Usage
        
        @Must(arg1=float, arg2=(list, float), arg3=(list,str))
        def someResourceMethod(self, request, params)
            params['arg1'] instanceof float
            params['arg2'] list of floats
            params['arg3'] list of str's
        
        if any arg fails to cast to the type correctly OR is missing, @Must returns instead
        dict(success = False, reason = "Missing {argName}" or "{argName cannot be convert to type {ArgType}})
    """
    def __init__(self, **expected):
        
        self.badCast = expected.pop('_badCast', "%s(%s) cannot be cast to %s")
        self.isMissing = expected.pop('_isMissing', "%s instanceof %s is required")
        self.expectations = expected
    
    def parseRequestArgs(self, request):
        missing = []
        badCast = []
        params = {}
        for name, desired in self.expectations.items():
            if name not in request.args:
                missing.append( self.isMissing % ( name, "%s" % desired )  )
                continue
            rawValue = request.args[name]
            #if desired type is list, we're done here
            value = None
            if isinstance(rawValue, desired):
                value = rawValue
            #instead of type checking, should probably do capability testing
            if isinstance(desired, tuple):
                base, ext = tuple
                if base == list:
                    value = []
                    for rawElement in rawValue:
                        try:
                            value.append(ext(rawElement))
                        except TypeError, e:
                            badCast.append(self.badCast % ( 'string', rawElement, ext )
            else:
                try:
                    value.append(ext(rawValue))
                except TypeError, e:
                    badCast.append(self.badCast % ( 'string', rawValue, ext )
           
            params[name] = value
            
        return (params, missing, badCast)    
            
        
    def __call__(self, host):
    
            
        @wraps(host)
        def wrapper(request)
            params, missing, badCast = self.parseRequest(request)
            success = True
            reason = ""
            if len(missing) > 0:
                success = False
                reason += "; ".join(missing)
            if len(badCast) > 0:
                success = False:
                reason += "; ".join(badCast)
                
            if success:
                return host
            else:
                return dict(success = success, reason = reason)
        
        return wrapper

       
class Can(object):
    """
        Similar to classs Must except if missing, it doesn't
        shortcircuit.  If it fails to cast, then it will error out
    """        
            

def isPOST(f):
    return RequestTypes.POST
    
def isGET(f):
    return RequestTypes.GET


class Controller(resource.Resource):
    
    def __init__(self):
        resource.Resource.__init__(self)
    
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
        
    