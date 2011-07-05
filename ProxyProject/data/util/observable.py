import copy 
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
    
    def observe(self, deferred):
        self.stack.append(deferred)
        
    def emit(self, *args, **kwargs):
        """
            To prevent the handler for a deferred putting the system
            into a death spiral, copy the stack, then assign a new list
            instance to self.stack
        """
        oldStack = copy.deepcopy(self.stack)
        self.stack = []
        while len(oldStack):
            #@todo can't remember if Twisted...deferred handles exceptions from
            #it's handlers
            deferred = oldstack.pop()
            deferred.callback(*args, **kwargs)
        