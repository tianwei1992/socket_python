"""application可以是可迭代对象"""

class AppClassIter(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        self.start_response(self.status, self.response_headers)
        yield b'Hello AppClass.__call__\n'
