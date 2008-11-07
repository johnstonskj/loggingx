import logging, unittest

import logtest
from loggingx.wef import WEFFormatter

class TestWEFLog(logtest.TestLoggerExtensions):
    """ Test the WEF logging extension to the common Python logging framework.
    """
    
    def setUp(self):
        logtest.TestLoggerExtensions.setUp(self)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(WEFFormatter())    
        self.logger.addHandler(handler)

if __name__ == '__main__':
    unittest.main()
