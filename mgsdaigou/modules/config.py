#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
@File    :   config.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2021/11/3         zhangyu 1.0         None
"""
import sys

# DB配置
DB_HOST = '127.0.0.1' if sys.platform.startswith('linux') else '39.99.248.97'
DB_PORT = 3306
DB_MAX_CONNECTIONS = 5
DB_MIN_CONNECTIONS = 1
DB_USER = 'sugar'
DB_PASSWORD = 'sugar123'
DB_NAME = 'dytt'

# redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_DB = 0

# 常量
DYTT_LINKS_KEY = 'DYTT_LINKS'
DYTT_NATION_KEY = 'DYTT_NATION'
DYTT_MOVIE_TYPE_KEY = 'DYTT_MOVIE_TYPE'
DYTT_NATION_TAGS_KEY = 'DYTT_NATION_TAGS'
DYTT_TYPE_TAGS_KEY = 'DYTT_TYPE_TAGS'
WITHOUT_LOGIN = 401

# zydg
ZYDG_HOMEPAGE = 'http://www.mgsdaigou88.vip'
ZYDG_ENCODING = 'utf8'
