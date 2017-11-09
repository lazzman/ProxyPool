# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379  # 默认端口
REDIS_PASSWORD = ''  # 如果有密码则填写密码，没有则为''

# 代理有效性校验周期（单位秒）
PROXY_CHECK_CYCLE = 60

# 代理池长度校验周期，当代理数量不在阈值内时会触发代理添加器
PROXU_POOL_LEN_CHECK_CYCLE = 20

# 代理池代理IP数量（上下限）
PROXY_POOL_LOWER_THRESHOLD = 20
PROXY_POOL_UPPER_THRESHOLD = 100

# 校验代理有效性的地址
CHECK_PROXY_USEFULL_URL = 'http://www.baidu.com'

# 检测代理有效性等待的超时时间(单位秒)
CHECK_PROXY_USEFULL_TIMEOUT = 9

import logging

# 控制台日志输出级别
LOGGING_LEVEL = logging.INFO
