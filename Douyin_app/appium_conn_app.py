'''
使用appium 链接抖音app
'''
from gevent import monkey
monkey.patch_all()

import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from Douyin_app.conn_DB import Handle_DB



class Handle_App(object):

    def __init__(self):
        self.param = {
                      "platformName": "Android",
                      "platformVersion": "7.1.1",
                      # "platformVersion": "5.1.1",
                      "platformVersion": "9",
                      # "deviceName": "8257a880",
                      "deviceName": "ZY223V45LX",
                      # "udid": "8257a880",
                      "udid": "ZY223V45LX",
                      # "deviceName": "21aa102803037ece",
                      "appPackage": "com.ss.android.ugc.aweme",
                      "appActivity": "com.ss.android.ugc.aweme.main.MainActivity",
                      "noReset": True,
                      "unicodekeyboard": True,
                      "resetkeyboard": True
                    }


        self.flag_timeout = 0

    def get_window_size(self):
        '''
        获取当前页面的尺寸
        :param driver:
        :return: width 和 height
        '''
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return (x,y)

    def swipe_screen(self):
        """
        滑动屏幕
        :param driver:
        :return:
        """
        x, y = self.get_window_size()
        # 定义滑动的坐标
        x_center = int(x * 0.5)
        y_start = int(y * 0.9)
        y_end = int(y * 0.2)

        while True:
            # 是否滑动到了最低端
            if '没有更多了' in self.driver.page_source:
                break
            # 是否有粉丝
            elif '还没有粉丝' in self.driver.page_source:
                break

            else:
                # 初始鼠标位置 x_center, y_start 结束位置 x_center, y_end
                self.driver.swipe(x_center, y_start, x_center, y_end)
                time.sleep(0.5)

    def back_to_search_page(self):
        try:
            if WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/n7")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/n7").click()
                time.sleep(0.1)
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/n7").click()
            # 清空搜索框的内容
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.ss.android.ugc.aweme:id/afo")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/afo").clear()
        except:
            pass

    def search_user(self, short_id):
        # 搜索用户
        try:
            # 往搜索框里写入id
            if self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/afo"):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/afo").send_keys(short_id)
            # 点击搜索按钮
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.ss.android.ugc.aweme:id/afr")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/afr").click()
            # 点击用户按钮
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.LinearLayout/android.widget.TextView")):
                self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[3]/android.widget.LinearLayout/android.widget.TextView").click()

            # 点用户详情页面
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.ss.android.ugc.aweme:id/blf")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/blf").click()

            # 查看用户的粉丝
            if WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/aj1")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/aj1").click()

                # 滑动屏幕
            self.swipe_screen()
            # 返回到搜索页面并且清空搜索框里的数据
            self.back_to_search_page()

        except:
            pass


    def go_search_page(self, short_id):

        try:
            # 点击初始状态的一些信息
            if self.driver.find_element_by_xpath("com.ss.android.ugc.aweme:id/bsr"):
                self.driver.find_element_by_xpath("com.ss.android.ugc.aweme:id/bsr").click()
            if self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/s8"):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/s8").click()
            if self.driver.find_element_by_xpath("//android.widget.TextView[@text='视频有音乐哦']"):
                self.driver.find_element_by_xpath("//android.widget.TextView[@text='视频有音乐哦']").click()
        except:
            pass
        try:
            # 点击放大镜按钮 进如到搜索页面
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.ss.android.ugc.aweme:id/apx")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/apx").click()
            if WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.ss.android.ugc.aweme:id/afo")):
                self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/afo").click()
                self.search_user(short_id=short_id)
        except:
            print('没找到搜索按钮')


    def start_app(self, short_id):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.param)
        self.go_search_page(short_id)
        while True:
            conn_db = Handle_DB()
            short_id = conn_db.get_short_id()
            print(short_id)
            self.search_user(short_id)


if __name__ == '__main__':

    is_first_run = True
    conn_db = Handle_DB()
    short_id = conn_db.get_short_id()
    print(short_id)
    Handle_App().start_app(short_id=short_id)


