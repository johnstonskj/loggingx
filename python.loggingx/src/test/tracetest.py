import logging, sys, unittest

from loggingx import trace
from tracetester import other

def test_func(i, s, l):
    trace.called()
    a = 99
    b = 'my word'
    trace.returning(1)
    return 1

class TestTraceLogging(unittest.TestCase):
    def runTest(self):
        trace.enable(True)
        test_func(1, 'hello', ['one', 'two'])      
        other.current_time()  
        other.test_optional('a', 'b')
        other.test_positional(1, 2, 3, 4)
        other.test_kwds(1, name='foor', other='bar', count=2)
        obj = other.TestClass()
        obj.method_one()

if __name__ == '__main__':
    unittest.main()
