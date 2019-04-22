import redis
import pymongo

def redis_demo():

    r = redis.Redis(host='localhost', port=6379)
    # print(r.sadd('ShortId', '12121212'))   #添加
    # print(r.sadd('ShortId', '12121212'))   #添加
    # print(r.sadd('ShortId', '121221212'))   #添加
    # print(r.sismember('ShortId', '121221212'))
    print(r.sismember('ShareId', share_id))
    # r.save()

def mongo_demo():

    mongo_db = pymongo.MongoClient('127.0.0.1', 27017)
    db = mongo_db['douyin']

    short_id_col = db['short_id']
    if short_id_col.find_one({}):

        print(short_id_col.find_one({})['short_id'])
    else:
        print('没有数据')

mongo_demo()