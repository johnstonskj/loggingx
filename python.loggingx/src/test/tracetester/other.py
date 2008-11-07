import datetime

from loggingx import trace

def current_time():
    trace.called()
    dt = datetime.datetime.now()
    trace.returning(dt)
    return dt

def test_optional(a, b, c=0, d=None):
    trace.called()
    
def test_positional(pos1, *posn):
    trace.called()

def test_kwds(pos1, **kwds):
    trace.called()
    
    
class TestClass(object):
    def method_one(self):
        trace.called()