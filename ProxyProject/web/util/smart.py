

from functools import wraps
from twisted.web import (server, resource )
from twisted.web.server import Request

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
    
    def parseRequestArgs(self, request, params = {}):
        missing = []
        badCast = []
        for name, desired in self.expectations.items():
            if name not in request.args:
                missing.append( self.isMissing % ( name, "%s" % desired )  )
                continue
            
            try:
                rawValue = request.args[name][0]
            except IndexError, e:
                rawValue = request.args[name]
                
            #if desired type is list, we're done here
            value = None
            if isinstance(desired, tuple):
                base, ext = desired
                if base == list:
                    value = []
                    for rawElement in rawValue:
                        try:
                            value.append(ext(rawElement))
                        except TypeError, e:
                            badCast.append(self.badCast % ( 'string', rawElement, ext ))
            else:
                try:
                    value = desired(rawValue)
                except TypeError, e:
                    badCast.append(self.badCast % ( 'string', rawValue, ext ))
           
            params[name] = value
            
        return (params, missing, badCast)    
            
        
    def __call__(self, host):
    
            
        @wraps(host)
        def wrapper(request, params = {}):
            params, missing, badCast = self.parseRequestArgs(request, params)
            success = True
            reason = ""
            if len(missing) > 0:
                success = False
                reason += "; ".join(missing)
            if len(badCast) > 0:
                success = False
                reason += "; ".join(badCast)
                
            return host(request, params) if success else dict(success = success, reason = reason)
            
        return wrapper

       
class Can(Must):
    """
        Similar to classs Must except if missing, it doesn't
        shortcircuit.  If it fails to cast, then it will error out
    """        
    def __call__(self, host):

        
        @wraps(host)
        def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            else:
                raise InvalidArgument("Missing Request object for wrapped action method call")                
                
            params, missing, badCast = self.parseRequestArgs(request, {})
            return host(*args, params = params)                            
        
        return wrapper
    
    
def isPOST(f):
    f.type = RequestTypes.POST
    return f
    
def isGET(f):
    f.type = RequestTypes.GET
    return f


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
        
    