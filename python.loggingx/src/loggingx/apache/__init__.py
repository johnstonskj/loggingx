"""
This module implements log formatters for the Apache common log format.
"""

import logging, sys

FORMAT_APACHE_DATE = '%d/%b/%Y %H:%M:%S'

FORMAT_ERROR_LOG = '[%(asctime)s] [%(levelname)s] [client %(remote)s] %(message)s'

FORMAT_COMMON_LOG = '%(remote)s - %(user)s [%(asctime)s] "%(method)s %(path)s%(query)s %(protocol)s" %(status)s %(size)s'

FORMAT_COMBINED_LOG = FORMAT_COMMON_LOG + '\n"%(referrer)s" "%(agent)s"'

__access_log = None
__error_log = None

def basicConfig(format=FORMAT_COMMON_LOG):
    """ Used to setup the two Apache loggers, each is configured by default
        with the correct record and date formats. Each logger is named and
        can therefore be used by other client directly (using logging.getLogger()).
        apache.access - the Apache common log
        apache.error - the Apache error log
    """
    global __access_log
    access_handler = logging.StreamHandler(sys.stderr)
    access_formatter = logging.Formatter(format, FORMAT_APACHE_DATE)
    access_handler.setFormatter(access_formatter)
    __access_log = logging.Logger('apache.access', logging.INFO)
    __access_log.addHandler(access_handler)
    global __error_log
    error_handler = logging.StreamHandler(sys.stderr)
    error_formatter = logging.Formatter(FORMAT_ERROR_LOG, FORMAT_APACHE_DATE)
    error_handler.setFormatter(error_formatter)
    __error_log = logging.Logger('apache.error', logging.WARNING)
    __error_log.addHandler(error_handler)

def log_wsgi_request(environ, code, size):
    """ Log a WSGI compliant request and response data, using the standard
        Apache configured logging objects. The environ parameter should
        be a standard WSGI request environment.
    """
    if environ:
        request_dict = {
            'remote': environ.get('REMOTE_HOST', environ.get('REMOTE_ADDR', None)),
            'user': environ.get('REMOTE_USER', ''),
            'method': environ.get('REQUEST_METHOD', None),
            'path': environ.get('PATH_INFO', None),
            'query': environ.get('QUERY_STRING', None),
            'protocol': environ.get('SERVER_PROTOCOL', None),
            'referrer': environ.get('HTTP_REFERER', ''),
            'agent': environ.get('HTTP_USER_AGENT', None),
            'status': code,
            'size': size}
        __access_log.info('', extra=request_dict)

def log_wsgi_error(environ, message):
    """ Log an error message, using the standard Apache configured logging 
        objects. The environ parameter should be a standard WSGI request 
        environment.
    """
    request_dict = {
        'remote': environ.get('REMOTE_HOST', environ.get('REMOTE_ADDR', None))}
    __error_log.error(message, extra=request_dict)
