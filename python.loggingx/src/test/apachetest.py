import unittest

from loggingx.apache import *

class TestApacheLogger(unittest.TestCase):
    """ Test the Apache logging extraction.
    """

    wsgi_request = {
         'REMOTE_HOST': 'localhost',
         'REMOTE_ADDR': '127.0.0.1',
         'REMOTE_USER': 'skjohn',
         'REQUEST_METHOD': 'GET',
         'PATH_INFO': '/',
         'QUERY_STRING': '',
         'SERVER_PROTOCOL': 'HTTP/1.1',
         'HTTP_USER_AGENT': 'Mozilla'}
    
    def testStandard(self):
        """ Call the logger methods directly """
        basicConfig()
        log_wsgi_request(self.wsgi_request, '', '')
        log_wsgi_error(self.wsgi_request, 'something really bad')
    
    def __testRunServer(self):
        """ Call the logger methods directly """
        basicConfig()
        def show_environ(environ, start_response):
            start_response('200 OK',[('Content-type','text/html')])
            sorted_keys = environ.keys()
            sorted_keys.sort()
            return [
                '<html><body><h1>Content in <tt>environ</tt></h1><p>',
                '<pre>'+str(environ)+'</pre>',
                '</p></body></html>',
            ]
            
        from wsgiref import simple_server
        httpd = simple_server.WSGIServer(
            ('',8000),
            simple_server.WSGIRequestHandler,
        )
        httpd.set_app(show_environ)
        httpd.serve_forever()            

if __name__ == '__main__':
    unittest.main()
