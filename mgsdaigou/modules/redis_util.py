"""
@File    :   redis_util.py
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2021/9/6        zhangyu 1.0         redis工具类
"""
import redis
from . import config


# 生成redis队列的key
def gen_redis_key(*args):
    return '_'.join(args)


# 从redis连接池中获取连接
def get_redis_pool():
    pool = redis.ConnectionPool(host=config.REDIS_HOST,
                                port=config.REDIS_PORT,
                                password=config.REDIS_PASSWORD,
                                db=config.REDIS_DB,
                                decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r


def get_redis_pool(r_db=0):
    pool = redis.ConnectionPool(host=config.REDIS_HOST,
                                port=config.REDIS_PORT,
                                password=config.REDIS_PASSWORD,
                                db=r_db,
                                decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r


# 获取指定redis
def get_redis(host, port, password, db):
    r = redis.Redis(host=host, port=port, password=password, db=db, decode_responses=True)
    return r

