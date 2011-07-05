
import unittest
from web.util.smart import *
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
        
            
                    
if __name__ == '__main__':
     unittest.main()
        
        
