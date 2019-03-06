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
    
    
