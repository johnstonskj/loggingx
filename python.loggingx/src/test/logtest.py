import logging, sys, unittest

class TestLoggerExtensions(unittest.TestCase):
    """ Base class for all logger tests.
    """
    def setUp(self):
        """ Setup common log parameters """
        logging.basicConfig(level=logging.DEBUG,
                            stream=sys.stdout)
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.DEBUG)
        
    def runTest(self):
        """ Common log test case """
        logging.info('My first example log message - just information.')
        self.logger.info('Another quick message, using self.logger.')
        logger1 = logging.getLogger('test.area1')
        logger1.debug('Here is a quick debug message, it should appear.')
        logger1.info('Another boring information message, with a "%s" parameter.' % 'string')
        logger1.info('Another boring message, with a "%s" parameter and arguments.' % 'string',
                     extra={'myname': 'simon', 'version': sys.version})
        logger2 = logging.getLogger('test.area2')
        logger2.warning('Hey, just a warning, check out behind you!')
        logger2.error('No really, TURN AROUND!')
        try:
            1/0
        except Exception, e:
            self.logger.exception("Oops, that didnt really work now did it.")