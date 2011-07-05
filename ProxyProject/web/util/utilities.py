from twisted.web.server import NOT_DONE_YET

from functools import wraps
from json import dumps

def jsonify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except Exception, e:
            return dict(success=False, message = "%s" % e )
        else:
            if response == NOT_DONE_YET:
                return response
            else:
                try:
                    return dumps(response)
                except Exception, e:
                    return dict(success=False, message = "%s" % e )
        
    
    return wrapper
