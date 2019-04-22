'''
配合 mitmdump 抓取数据
'''
import json

try:
    from Douyin_app.conn_DB import Handle_DB
except:
    from conn_DB import Handle_DB

def response(flow):
    '''
    这个函数是mitmdump的固定写法 启动方法 ：mitmdump -s py_path -p 8889
    :param flow:抓取到的数据流
    :return:
    '''
    mongod = Handle_DB()
    if 'follower/list' in flow.request.url:
        print(flow.response.text)
        data = json.loads(flow.response.text)
        followers = data['followers']
        # 把获取的粉丝信息逐个存到数据库
        for user in followers:
            short_id = {}
            if len(user['uid']) > 1:
                short_id['share_id'] = user['uid']

            mongod.insert_mitmdump_data(short_id)
            print(short_id)


