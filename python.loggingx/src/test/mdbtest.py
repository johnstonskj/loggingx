import logging, os, sys, unittest

import logtest
from loggingx.db import DatabaseHandler

class MultiTestDatabaseLog(logtest.TestLoggerExtensions):
    """ Test the DB logging extension to the common Python logging
        framework, using multiple sub-processes.
    """
    
    def setUp(self):
        logtest.TestLoggerExtensions.setUp(self)
        handler = DatabaseHandler()
        self.logger.addHandler(handler)
        
    def runTest(self):
        for index in range(3):
            logging.info('About to run test %d' % index)
            pid = os.spawnl(os.P_NOWAIT, sys.executable, 'python', 'dbtest.py')
            logging.info('Test %s running' % str(pid))

if __name__ == '__main__':
    unittest.main()
