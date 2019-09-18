一、前言
gunicorn是目前使用最广泛的高性能的Python WSGI（WEB Server Gateway interface）服务器，移植自Ruby的Unicorn项目，使用pre-fork worker模式，具有简单、易用、轻量级、低资源消耗和高性能等特点。

二、参数说明
2.1 启动参数说明
-c CONFIG, --config=CONFIG		指定配置文件
-b BIND, --bind=BIND		绑定运行的主机加端口
-w INT, --workers INT		用于处理工作进程的数量，整数，默认为1
-k STRTING, --worker-class STRTING		要使用的工作模式，默认为sync异步，类型：sync, eventlet, gevent, tornado, gthread, gaiohttp
--threads INT		处理请求的工作线程数，使用指定数量的线程运行每个worker。为正整数，默认为1
--worker-connections INT		最大客户端并发数量，默认1000
--backlog int		等待连接的最大数，默认2048
-p FILE, --pid FILE		设置pid文件的文件名，如果不设置将不会创建pid文件
--access-logfile FILE		日志文件路径
--access-logformat STRING		日志格式，--access_log_format '%(h)s %(l)s %(u)s %(t)s'
--error-logfile FILE, --log-file FILE		错误日志文件路径
--log-level LEVEL		日志输出等级
--limit-request-line INT		限制HTTP请求行的允许大小，默认4094。取值范围0~8190，此参数可以防止任何DDOS攻击
--limit-request-fields INT		限制HTTP请求头字段的数量以防止DDOS攻击，与limit-request-field-size一起使用可以提高安全性。默认100，最大值32768
--limit-request-field-size INT		限制HTTP请求中请求头的大小，默认8190。值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制
-t INT, --timeout INT		超过设置后工作将被杀掉并重新启动，默认30s，nginx默认60s
--reload		在代码改变时自动重启，默认False
--daemon		是否以守护进程启动，默认False
--chdir		在加载应用程序之前切换目录
--graceful-timeout INT		默认30，在超时(从接收到重启信号开始)之后仍然活着的工作将被强行杀死；一般默认
--keep-alive INT		在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间
--spew		打印服务器执行过的每一条语句，默认False。此选择为原子性的，即要么全部打印，要么全部不打印
--check-config		显示当前的配置，默认False，即显示
-e ENV, --env ENV		设置环境变量


2.2 配置文件示例
-c CONFIG, --config=CONFIG
配置文件方式
vim gunicorn.conf
```
# 并行进程数
workers = 4

# 指定每个工作的线程数
threads = 2

# 监听端口8000
bind = '127.0.0.1:8000'

# 守护进程,将进程交给supervisor管理
daemon = 'false'

# 工作模式协程
worker_class = 'gevent'

# 最大并发量
worker_connections = 2000

# 进程文件
pidfile = '/var/run/gunicorn.pid'

# 访问日志和错误日志
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'

# 日志级别
loglevel = 'debug'

# 并行进程数
workers = 4
 
# 指定每个工作的线程数
threads = 2
 
# 监听端口8000
bind = '127.0.0.1:8000'
 
# 守护进程,将进程交给supervisor管理
daemon = 'false'
 
# 工作模式协程
worker_class = 'gevent'
 
# 最大并发量
worker_connections = 2000
 
# 进程文件
pidfile = '/var/run/gunicorn.pid'
 
# 访问日志和错误日志
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'
 
# 日志级别
loglevel = 'debug'
```