""" Trace functions.
"""

import inspect, logging, types

LVL_TRACE = 5
LVL_TRACE_NAME = 'TRACE'

logging.addLevelName(LVL_TRACE, LVL_TRACE_NAME)
logging.basicConfig()
_logger = logging.getLogger('root')

def enable(yes):
    if yes:
        _logger.setLevel(LVL_TRACE)
    else:
        _logger.setLevel(logging.CRITICAL)
        
def called():
    if _logger.isEnabledFor(LVL_TRACE):
        frame = inspect.currentframe().f_back
        cls = ''
        function = frame.f_code.co_name
        module = inspect.getmodule(frame.f_code).__name__
        try:
            # is this a class method?
            the_class = frame.f_locals[frame.f_code.co_varnames[0]] 
            if (isinstance(the_class, types.ClassType) or
                isinstance(the_class, types.ObjectType)):
                method = getattr(the_class, function)
                if method.im_func.func_code == frame.f_code:
                    module = module + '.%s' % the_class.__class__.__name__
        except:
            pass
        (args, varargs, varkw, locals) = inspect.getargvalues(frame)
        values = inspect.formatargvalues(args, varargs, varkw, locals)
        _logger.log(LVL_TRACE, '%s.%s%s' % (module, function, values))
        del frame

def returning(value):
    if _logger.isEnabledFor(LVL_TRACE):
        frame = inspect.currentframe().f_back
        function = frame.f_code.co_name
        module = frame.f_globals[function].__module__
        _logger.log(LVL_TRACE, '%s.%s(...) -> %s' % (module, function, repr(value)))
        del frame
