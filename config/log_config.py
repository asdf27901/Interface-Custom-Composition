# -*- encoding: utf-8 -*-
# Author: Roger·J
# Date: 2022/4/12 5:06 PM
# File: log_config.py

import os

# 定义日志输出格式 结束
simple_format = '%(asctime)s - %(levelname)-7s - %(filename)s - %(lineno)4d - %(threadName)s - %(message)s'

path = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logfile_dir = path('../log/')     # log文件的目录

logfile_name = 'test.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': simple_format,
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'consoleHandler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'fileHandler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
            'formatter': 'simple',
            'filename': logfile_path,
            'when': 'midnight',
            'interval': 1,
            'backupCount': 0,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        '': {
            'handlers': ['consoleHandler', 'fileHandler'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}
