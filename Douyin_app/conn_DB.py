"""
mongo数据库读写
"""
import pymongo
import redis

class Handle_DB(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        client = pymongo.MongoClient(self.host, self.port)
        self.db = client['douyin']
        # 链接redis数据库
        self.r = redis.Redis(host='localhost', port=6379)


    def insert_share_data_by_local(self):
        """
        从本地文件douyin_hot_id.txt中读取分享ID，写入到数据库
        :return:
        """
        # db = self.conn_mongo()
        share_id_col = self.db['share_id']
        # db_collation = Collation(db, 'share_id')
        with open('douyin_hot_id.txt', 'r') as f:
            for data in f.readlines():
                share_id = {}
                share_id['id'] = data.replace('\n', '')
                share_id_col.insert(share_id)

    def insert_personal_info(self, data):
        '''
        插入从分享页面解析到的个人信息
        :param data:
        :return:
        '''
        # db = self.conn_mongo()
        share_id_col = self.db['personal_info']
        share_id_col.insert(data)

    def insert_shareid_to_redis(self, share_id):
        '''
        把分享ID插入到redis
        :param share_id:
        :return:
        '''
        self.r.sadd('ShareId', share_id)

    def insert_shortid_to_mongo(self, short_id):
        # 把抖音ID存入到short_id
        shortid = {}
        short_id_col = self.db['short_id']
        shortid['short_id'] = short_id
        short_id_col.insert(shortid)

    def get_short_id(self):
        '''
        从数据库中取出一条抖音ID数据并删除
        :return:
        '''
        # db = self.conn_mongo()
        short_id_col = self.db['short_id']
        # 数据库里可能没有数据
        if short_id_col.find_one({}):
            # print(short_id_col.find_one_and_delete({}))
            return short_id_col.find_one_and_delete({})['short_id']
        else:
            return False

    def get_share_id(self):
        '''
        从数据库中取出一条分享ID数据并删除
        :return:
        '''
        share_id_col = self.db['share_id']

        _share = share_id_col.find_one_and_delete({})['share_id']
        # 判断是否有数据
        if _share:
            return _share
        else:
            return False

    def insert_mitmdump_data(self, data):
        '''
        从mitmdump抓到数据存到数据库中
        :param data:
        :return:
        '''
        # db = self.conn_mongo()

        share_id_col = self.db['share_id']
        share_id_col.insert(data)


    def is_share_id_parsed(self, share_id):
        """
        在redis数据库中判断数据是否已经解析过
        """
        return self.r.sismember('ShareId', share_id)

if __name__ == '__main__':

    # Handle_Mongodb().insert_share_data_by_local()
    print(Handle_DB().get_share_id())