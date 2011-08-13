import copy
from twisted.internet.defer import Deferred
class Observable(object):
    """
        A dirt simple observable that can collect multiple
        deferreds and discharge them.
        
        On emit, all deferreds have their callback's fired
        and then the deferred is popped out, making it the    
        responsibility of the deferred's origin to reapply
    """
    
    def __init__(self):
        self.stack = []
        self.deferred = Deferred()
     
    def __call__(self, *args):
        for arg in args:
            self.deferred.addCallback(arg)
        return self.deferred
    
    def emit(self, result):
        """
            To prevent the handler for a deferred putting the system
            into a death spiral, copy the stack, then assign a new list
            instance to self.stack
        """
        newDefer = Deferred()
        oldDefer = self.deferred
        self.deferred = newDefer
        oldDefer.callback( result ) 
            
            