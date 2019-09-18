# -*-coding:utf-8 -*-

__author__ = "YC"

import os
import multiprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
chdir = BASE_DIR

# 监听本机的5000端口
bind = '0.0.0.0:6060'

# 开启进程
workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程的开启线程
threads = multiprocessing.cpu_count() * 2

# 等待连接的最大数
backlog = 2048

#工作模式为meinheld
worker_class = "egg:meinheld#gunicorn_worker"

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
daemon = False

# 进程名称
# proc_name = 'gunicorn.pid'
proc_name = os.path.join(BASE_DIR, 'log', 'gunicorn.pid')

# 进程pid记录文件
pidfile = os.path.join(BASE_DIR, 'log', 'app.pid')
logfile = os.path.join(BASE_DIR, 'log', 'debug.log')

# 要写入的访问日志目录
accesslog = os.path.join(BASE_DIR, 'log', 'access.log')
# 要写入错误日志的文件目录。
errorlog = os.path.join(BASE_DIR, 'log', 'error.log')
# print(BASE_DIR)

# 日志格式
# access_log_format = '%(h)s %(t)s %(U)s %(q)s'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

#  日志等级
loglevel = 'debug'