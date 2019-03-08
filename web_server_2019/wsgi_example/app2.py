"""application可以是实现了_call方法的类的实例，之哟啊是可调用对象就行"""

class AppClass(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __call__(self, environ, start_response):
        print(environ, start_response)
        start_response(self.status, self.response_headers)
        return [b'Hello AppClass.__call__\n']

application = AppClass()