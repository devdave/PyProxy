import unittest
from twisted.web.test.test_web import DummyRequest
from ProxyProject.web.controllers.simple import Simple

class MockStore(object):
    data = {}
    hostCount = {}

#class TestControllersSimple(unittest.TestCase):
#
#    def setUp(self):
#        self.simple = Simple()
#        self.simple.myStore = MockStore()
#
#    def test_nondeferred_host_count(self):
#        request = DummyRequest([''])
#        response = self.simple.do_host_count(request)