# Socket学习笔记

## 单线程socket
1. 启动端口复用，一个IP+PORT才能够复用多次
2. 单线程下用sleep（60）模拟执行任务，在浏览器看到正在等待响应,而另一个客户端还在外面等待。
3. 'Content-Type: text/html'与'Content-Type: text/plain'的区别。

## 多线程socket
1. 非阻塞的socket：

    * 会不断地轮询，于是accpet()不到对端以及conn.recv()收不到数据的时候都会报错BlockingIOError
    * linux上叫做errno.EAGAIN，windows上叫做errno.EWOULDBLOCK。

        `BlockingIOError: [WinError 10035] 无法立即完成一个非阻止性套接字操作。`
    
    * 其实是异常不是错误，accpet()用except-continue继续就行。
    * 那么recv()怎么处理好呢？conn.close()吗？

2. 阻塞&非阻塞

    * 这里既然有多线程or多进程，所以用阻塞socket也可以实现并发
    * 非阻塞socket一般搭配异步 -> 异步非阻塞 
    
## WSGI协议
协议分为2部分：Web app和Web Server（Gateway）
 
server将数据按照WSGI规定的方式传给app，app的处理就是要设置status和header并返回body，最后由server进行http协议的封装。
 1. 各模块功能说明
     1. app.py只需要定义一个simple_app(),参数限定为environ和start_response
     2. gateway.py从app.py拿到simple_app，然后就从run_with_cgi(simple_app)开始执行。
     
        #### run_with_cgi(simple_app)的执行过程
        1. 收集环境变量
        2. 执行result = simple_app(environ, start_response)，其中会又会回调gateway.py中定义的start_response()产生status和response_headers（但没有发出去），还有body返回保存于result。
        3. 发送数据
     3. 回调函数start_response()在gateway中定义，被application回调，主要作用是设置header.
     4. app.py所定义的application只要是可调用对象就行，可以是函数，也可以是实现__call__()方法的类的实例.
        application()会被调用返回result是响应的body，其执行中回调的start_response()会设置好status和header的值。
 2. 使用gunicorn提供的web server也可以启动app
    ```
    pip install gunicorn
    gunicorn app:simple_app
    gunicorn app3:AppClassIter &
    ```  
 3. gateway.py和gunicorn的共同结构
    1. 都要定义start_response()用于设置header，header的值都由app提供，这个函数也是在app的application()的调用中被作为第二个参数传入然后回调的。
    2. 启动时候，第一步获取环境变量，第二步就是调用application()获得body_list，第三步是发送响应。
    
 4. WSGI中间件（如Werkzeug）
 
    之前是先start_response()设置header，然后再返回body，没有统一。
    
    WSGI中间件就是直接封装在一个Response对象里面，最后带着header和body的信息一起返回：Response实例在创建时即传入body和start_response作为参数，也包含一个set_header方法可以调用start_response将header设置并绑定在自己身上。
 
          
