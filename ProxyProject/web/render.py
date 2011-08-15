

import mako
import mako.lookup
import cache
import static
from os.path import exists

makoLookup = mako.lookup.TemplateLookup(directories = [ static.relPath(".") ], module_directory = cache.MAKO_C, output_encoding="ascii" )


def byMako(path, **kwargs):
    
    if not path.endswith(".mako"):
        path += '.mako'
    truePath = static.relPath(path)
    assert exists(truePath), "Template file %s doesn't exist at %s" % ( path, truePath )
    template = makoLookup.get_template( path )
    return template
    
from functools import wraps

class asMako(object):
    def __init__(self, path):
        """
            Decorator to wrap an action, expects action to output a dictionary with
            requisite view parameters.
        """
        self.path = path
        
    
    def __call__(self, func):
    
        @wraps(func)
        def decorator(*args, **kwargs):
            response = func(*args, **kwargs)
            return byMako(self.path).render(**response)
            
        return decorator
            
        