
import unittest
from ProxyProject.web.util.smart import *
from twisted.web.test.test_web import DummyRequest


class TestUtilSmartMust(unittest.TestCase):

    def testMustSucceeds(self):
    
        expectedArg = 'hello'
        @Must(arg1 = str)
        def testMethod(request, params):
            self.assertTrue('arg1' in params)
            self.assertEqual(params['arg1'], expectedArg)
            
            
        request = DummyRequest([''])
        request.addArg('arg1', expectedArg)
        
        testMethod(request)
        
    def testMustSucceedsMultipleArgs(self):
        
        expectedArg1 = "hello"
        expectedArg2 = 123.4
        
        @Must(arg1 = str, arg2 = float )
        def testMethod(request, params):
            self.assertTrue('arg1' in params)
            self.assertTrue('arg2' in params)
            self.assertEqual(params['arg1'], expectedArg1)
            self.assertEqual(params['arg2'], expectedArg2)
            
        request = DummyRequest([''])
        request.addArg('arg1', expectedArg1)
        request.addArg('arg2', expectedArg2)
        
        testMethod(request)

    def testMustMissingArg1(self):

        @Must(arg1 = str)
        def testMethod(request, params):
            pass
            
            
        request = DummyRequest([''])
        
        response = testMethod(request)
        
        self.assertFalse(response['success'])
        self.assertEquals(response['reason'], "arg1 instanceof <type 'str'> is required")
        
    def testMustSucceedsWithListForArg1(self):
        
        @Must(arg1 = (list, float) )
        def testMethod(request, params):
            self.assertTrue('arg1' in params)
            self.assertTrue(len(params['arg1']) == 2)
            self.assertTrue(isinstance(params['arg1'][0], float))
            pass
        
        request = DummyRequest([''])
        request.addArg('arg1', ['123.5', '678.9'])
        
        response = testMethod(request)
        
                    
if __name__ == '__main__':
     unittest.main()
        
        
