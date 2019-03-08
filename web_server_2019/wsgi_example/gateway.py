# 这是一个CGI脚本

import os
import sys

"""app可以是函数，可以是实现了__call__()方法的类的实例，也可以是可迭代对象"""
from app import simple_app
from app2 import application  as simple_app2
from app3 import AppClassIter  as simple_app3

def wsgi_to_bytes(s):
    return s.encode('utf-8')


def run_with_cgi(application):
    environ = dict(os.environ.items())
    environ['wsgi.input'] = sys.stdin.buffer
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi._run_once'] = FutureWarning

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        """写响应的数据，如果是第一次，那么先写头部，再写body，否则直接写body"""
        out = sys.stdout.buffer   #所以打印到屏幕

        if not headers_set:    # 调用wirte应该在start_response之后，所以headers_set应该已经设置好
            raise AssertionError("write() before start_response()")
        elif not headers_sent:   #如果write是第一次被调用，那么先写头部
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status:{}\r\n'.format(status)))
            for header in response_headers:
                out.write(wsgi_to_bytes('%s:%s\r\n' % header))    #每个header之间要加上换行
            out.write(wsgi_to_bytes('\r\n'))    #header之后和body之前有一个换行

        # 之后再正式写data
        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        """首次设置headers_set,并返回方法write

        如果headers_set已设置或已发送，会引发异常"""
        if exc_info:
            try:
                if headers_sent:
                    raise (exc_info[0], exc_info[1], exc_info[2])
            finally:
                exc_info = None
        elif headers_set:
            print("in")
            raise AssertionError('Headers already set!')

        headers_set[:] = [status, response_headers]
        return write

    result = application(environ, start_response)   # 会回调start_response，设置header

    try:
        for data in result:
            if data:
                write(data)
        if not headers_sent:
            print("never")
            """如果result为空，表示write()从来没有被调用过"""
            write(b'')
    finally:
        if hasattr(result, 'close'):
            result.close()


if __name__ == "__main__":
    run_with_cgi(simple_app3)