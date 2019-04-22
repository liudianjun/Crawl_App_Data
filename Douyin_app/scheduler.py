'''
使用gevent(协程)自动调度
'''
# 把monkey.patch_all()放在调用之前，不然会有警告
import gevent
from gevent import monkey
monkey.patch_all()
from Douyin_app.conn_DB import Handle_DB
from Douyin_app.appium_conn_app import Handle_App
from Douyin_app.parse_share_content import Parse_Share_page
import time


class Main_Scheduler(object):

    def __init__(self):
        self.conn_db = Handle_DB()
        # 定义标志位 如果多次没有拿到数据协程结束
        self.flag_parse_timeout = 0
        self.parse_data = Parse_Share_page()

    def scheduler_app(self):
        is_first_run = True
        conn_db = Handle_DB()
        short_id = conn_db.get_short_id()
        print(short_id)
        Handle_App().start_app(short_id=short_id)

    def scheduler_Mongo(self):
        pass

    def scheduler_parse_page(self):

        conn_db = Handle_DB()
        while True:
            # 从数据库中获取分享ID
            share_id = conn_db.get_share_id()
            # Parse_Share_page(share_id).get_proxy()
            # print(share_id)
            # 如果取到数据，则解析
            if share_id:
                parse_data = Parse_Share_page()
                personal_info = parse_data.parsed_data_insert_db(conn_db, share_id)
            else:
                time.sleep(1)


if __name__ == '__main__':
    # Main_Scheduler().scheduler_app()
    # 使用协程并发处理数据
    gevent.joinall([

        gevent.spawn(Main_Scheduler().scheduler_parse_page),
        gevent.spawn(Main_Scheduler().scheduler_parse_page),

        # gevent.spawn(Main_Scheduler().scheduler_app),

    ])


