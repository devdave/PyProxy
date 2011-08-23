

from functools import wraps
from twisted.web import (server, resource )
from twisted.web.server import Request
from twisted.web.test.test_web import DummyRequest



    
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
    
    def findRequest(self, args):
        for arg in args:
            if isinstance(arg, Request) or isinstance(arg, DummyRequest):
                return arg                
        else: # pragma: no cover           
            raise Exception("Missing Request object for wrapped action method call")
            
    
    def parseRequestArgs(self, request, params = {}):
        missing = []
        badCast = []
        for name, desired in self.expectations.items():
            if name not in request.args:
                missing.append( self.isMissing % ( name, "%s" % desired )  )
                continue
            
            try:
                rawValue = request.args[name][0]
            except IndexError, e: # pragma: no cover
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
                        except TypeError, e: # pragma: no cover
                            badCast.append(self.badCast % ( 'string', rawElement, ext ))
            else:
                try:
                    value = desired(rawValue)
                except (ValueError, TypeError), e: # pragma: no cover
                    badCast.append(self.badCast % ( '<string>', rawValue, desired ))
                    continue
           
            params[name] = value
            
        return (params, missing, badCast)    
            
        
    def __call__(self, host):
    
            
        @wraps(host)
        def wrapper(*args, **kwargs):
            params = kwargs.get('params', dict() )
            #Let the Invalid exception bubble past here
            request = self.findRequest(args)

            params, missing, badCast = self.parseRequestArgs(request, params)
            success = True
            reason = ""
            if len(missing) > 0:
                success = False
                reason += "; ".join(missing)
            if len(badCast) > 0:
                success = False
                reason += "; ".join(badCast)
                
            return host(*args, params = params) if success else dict(success = success, reason = reason)
            
        return wrapper

       
class Can(Must):
    """
        Similar to classs Must except if missing, it doesn't
        shortcircuit.  If it fails to cast, then it will error out
    """        
    def __call__(self, host):

        
        @wraps(host)
        def wrapper(*args, **kwargs):
            #Let the Invalid exception bubble past here
            params = kwargs.get('params', dict() )
            request = self.findRequest(args)
                                           
            params, missing, badCast = self.parseRequestArgs(request, params)
            return host(*args, params = params)                            
        
        return wrapper
    
    