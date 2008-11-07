import logging, unittest

import logtest
from loggingx.db import DatabaseHandler

class TestDatabaseLog(logtest.TestLoggerExtensions):
    """ Test the DB logging extension to the common Python logging framework.
    """
    
    def setUp(self):
        logtest.TestLoggerExtensions.setUp(self)
        handler = DatabaseHandler()
        self.logger.addHandler(handler)

if __name__ == '__main__':
    unittest.main()
