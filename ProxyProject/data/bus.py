"""
  A DIRT simple message bus
  Rules for usage
     To prevent the application turning into a programmatic
     snakes and ladders or call spaghetti... Receiver should be named
     like moduleName.className or moduleName.defName atleast making it
     visibly understandable that
     bus.all("foo.ProcessThis") is generally going to be going to an instance
     of foo.ProcessThis where foo has been instantiated in main.py or some other
     central startup point.  Still not perfect but meh
"""
from collections import defaultdict
channels = defaultdict(list)

def registerSingle(name, callback):
    """
        Similar to register but ensures only one callback is register to a channel
        @todo change Exception to something more appropriate
        
        :name str A reasonably coherent name for a callback channel
        :callback callable Either a bound method or just a function
    """
    global channels
    if len(channels[name]) > 0:
        raise Exception("Tried to register %s but already has %s registered" % ( name, channels) )
    channels[name].append(callback)
    
def register(name, callback):
    """
        Binds a callback to a named channel
        
        :name str A reasonably coherent name for a callback channel
        :callback callable Either a bound method or just a function
    """
    global channels
    channels[name].append(callback)
    
    
def call(name, *args, **kwargs):
    """
        Applies the provided arguments to any and all callbacks for a specified channel
        
        :name str A reasonably coherent name for a callback channel
    """
    for callback in channels[name]:
        callback(*args, **kwargs)
    
def first(name, default = lambda : False):
    """
        Returns the first callback for a chanel
        
        :name str A reasonably coherent name for a callback channel
        :default To avoid exceptions and provided a fallback handler
    """    
    return channels.get(name, default)
    
def all(name):
    """
        Generator to allow for finer grained control over the process of calling a channel
        handler
        
        :name str A reasonably coherent name for a callback channel
        
    """    
    for callback in channels[name]:
        yield name
        
        
def clear():
    global channels
    channels = defaultdict(list)
    
        