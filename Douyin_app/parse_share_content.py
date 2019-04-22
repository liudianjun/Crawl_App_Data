'''
从分享ID中解析个人数据
'''
from gevent import monkey
monkey.patch_all()

import requests
import re
from lxml import etree
from Douyin_app.conn_DB import Handle_DB
import time
from Douyin_app.proxy_model import ProxyModel
import json


class Get_Proxy(object):

    def get_proxy(self):
        '''
        获取代理
        :return:
        '''
        proxys = {}
        get_ip_url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions='
        resp = requests.get(get_ip_url)
        result = json.loads(resp.text)
        print(result)
        try:
            proxy = ProxyModel(result['data'][0]).proxy
            proxys['http'] = proxy
            proxys['https'] = proxy
            # print(proxys)
            return proxys
        except:
            pass

PROXY = Get_Proxy().get_proxy()
class Parse_Share_page(object):

    # def __new__(cls):
    #     # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Parse_Share_page, cls).__new__(cls)
    #     return cls.instance

    def __init__(self):
        # 数字解密
        self.regex_list = [
        {'name':[' &#xe603; ',' &#xe60d; ',' &#xe616; '],'value':0},
        {'name':[' &#xe602; ',' &#xe60e; ',' &#xe618; '],'value':1},
        {'name':[' &#xe605; ',' &#xe610; ',' &#xe617; '],'value':2},
        {'name':[' &#xe604; ',' &#xe611; ',' &#xe61a; '],'value':3},
        {'name':[' &#xe606; ',' &#xe60c; ',' &#xe619; '],'value':4},
        {'name':[' &#xe607; ',' &#xe60f; ',' &#xe61b; '],'value':5},
        {'name':[' &#xe608; ',' &#xe612; ',' &#xe61f; '],'value':6},
        {'name':[' &#xe60a; ',' &#xe613; ',' &#xe61c; '],'value':7},
        {'name':[' &#xe60b; ',' &#xe614; ',' &#xe61d; '],'value':8},
        {'name':[' &#xe609; ',' &#xe615; ',' &#xe61e; '],'value':9},
    ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        # self.share_id = share_id
        # self.conn_mongo = Handle_DB()
        self.flag_timeout = 0
        # self.proxy_ip = PROXY


    def start_request(self, share_id):
        """
        请求数据
        :return: response.text
        """
        # 构造请求ID
        share_url = 'https://www.douyin.com/share/user/{}'.format(share_id)
        response = ''
        global PROXY
        try:
            response = requests.Session().get(share_url, proxies=PROXY,headers=self.headers).text
        except Exception as e:
            print('------{}-------'.format(e))
            response = requests.Session().get(share_url, proxies=PROXY,headers=self.headers).text
        if '页面不见啦' in response:
            print('<---IP被封，请求新IP--->')
            print('等待重新请求代理')
            time.sleep(3)
            PROXY = Get_Proxy().get_proxy()
            response = requests.Session.get(share_url, proxies=PROXY, headers=self.headers).text

        print('当前IP：', PROXY)

        data_dict = self.replace_ttf(response, share_id)
        return data_dict
        # print(response.text)


    def replace_ttf(self, response, share_id):
        """
        对加密的数字进行替换
        :return: 加密数字替换后的响应内容
        """
        response_data = ''
        for i in self.regex_list:
            for i2 in i['name']:
                response = re.sub(i2, str(i['value']), response)
                # print(i2, i['value'])
        with open('text.html', 'w') as f:
            f.write(response)

        data_dict = self.parse_page(response, share_id)

        return data_dict



    def parse_page(self, response_data, share_id):
        '''
        解析分享页面
        :return:
        '''
        global PROXY

        data_dict = {}

        etree_data = etree.HTML(response_data)
        data_dict['nickname'] = ''.join(etree_data.xpath("//p[@class='nickname']/text()"))
        if not data_dict['nickname']:
            # 重新请求
            print('-' * 50)
            print(share_id)
            with open('data.htlm', 'w') as f:
                f.write(response_data)

            print('等待重新请求代理')
            time.sleep(2)
            PROXY = Get_Proxy().get_proxy()
            print('重新请求', share_id)
            print('-'*50)
            return self.start_request(share_id)

        else:
            data_dict['share_id'] = share_id
            shortid_1 = etree_data.xpath("//p[@class='shortid']/text()")
            shortid_2 = etree_data.xpath("//p[@class='shortid']//i//text()")
            if len(shortid_1) > 1:
                shortid_1 = shortid_1[0].split(' ')[-1]
            else:
                shortid_1 = ''
            shortid_2 = str(''.join(shortid_2))
            # print(shortid_1, shortid_2)
            data_dict['shortid'] = shortid_1 + shortid_2
            data_dict['signature'] = ''.join(etree_data.xpath("//p[@class='signature']/text()"))
            data_dict['focus'] = str(''.join(etree_data.xpath("//p[@class='follow-info']/span[1]/span[1]/i//text()")))
            if 'w' in ''.join(etree_data.xpath("//p[@class='follow-info']/span[2]//text()")):
                # print((etree_data.xpath("//p[@class='follow-info']/span[2]/span[1]/i//text()")))
                data_dict['fans'] = str(
                    int(''.join(etree_data.xpath("//p[@class='follow-info']/span[2]/span[1]/i//text()"))) / 10) + 'w'
            else:
                data_dict['fans'] = str(
                    ''.join(etree_data.xpath("//p[@class='follow-info']/span[2]/span[1]/i//text()")))

            if 'w' in ''.join(etree_data.xpath("//p[@class='follow-info']/span[3]//text()")):
                data_dict['liked_num'] = str(
                    int(''.join(etree_data.xpath("//p[@class='follow-info']/span[3]/span[1]/i//text()"))) / 10) + 'w'
            else:
                data_dict['liked_num'] = str(
                    ''.join(etree_data.xpath("//p[@class='follow-info']/span[3]/span[1]/i//text()")))

            data_dict['location'] = ''.join(etree_data.xpath("//span[@class='location']/text()"))
            data_dict['constellation'] = ''.join(etree_data.xpath("//span[@class='constellation']/text()"))

            print('data_dict', data_dict)
            return data_dict

    def parsed_data_insert_db(self,conn_db, share_id):
        # 在redis中判断这个用户是否已经被解析过
        if conn_db.is_share_id_parsed(share_id):
            print('这条用户信息已解析')
            pass
        else:
            # print('解析用户信息')
            # 解析分享页面
            parse_data = Parse_Share_page()
            personal_info = parse_data.start_request(share_id)
            # 把解析到的个人数据存入到数据库
            # print('personal_info', personal_info)
            conn_db.insert_personal_info(personal_info)
            conn_db.insert_shortid_to_mongo(personal_info['shortid'])
            conn_db.insert_shareid_to_redis(personal_info['share_id'])
            time.sleep(0.5)


if __name__ == '__main__':

    conn_db = Handle_DB()
    # while True:
    # 从数据库中获取分享ID
    share_id = conn_db.get_share_id()
    # Parse_Share_page(share_id).get_proxy()
    print(share_id)
    # 如果取到数据，则解析
    if share_id:
        parse_data = Parse_Share_page()
        personal_info = parse_data.parsed_data_insert_db(conn_db, share_id)
    else:
        print('没有分享ID')
        time.sleep(1)

