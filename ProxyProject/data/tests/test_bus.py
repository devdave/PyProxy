import nose
from nose import with_setup
import unittest
from unittest import TestCase
import ProxyProject.data.bus as bus


@with_setup(bus.clear)
def test_registerCallback():
    name = "simpleTest"
    callback = lambda: True
    bus.registerSingle(name, callback)
    assert bus.channels[name][0] == callback, "First element should equal are callback"
        
        
@with_setup(bus.clear)
def test_registerMultipleCallbacks():
    name = "simpleTest"
    callbacks = [ lambda: True, lambda: True, lambda: True]
    for cb in callbacks:
        bus.register(name, cb)
        
    
    for i in range(len(callbacks)):
        assert callbacks[i] in bus.channels[name]
            
    
@nose.with_setup(bus.clear)
#@unittest.expectedFailure
@nose.tools.raises(Exception)
def test_registerSingleThrowsException():
    name = "simpleTest"
    callback = lambda: True
    
    bus.registerSingle(name, callback)
    bus.registerSingle(name, callback)
        
if __name__ == '__main__':
    nose.main()
