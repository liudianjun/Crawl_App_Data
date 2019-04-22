from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class Crwal_App_douyin(object):
    def __init__(self):
        self.representation_data ={
                "platformName": "Android",
                "deviceName": "127.0.0.1:62001",
                "appPackage": "com.ss.android.ugc.aweme",
                "appActivity": ".main.MainActivity"
            }

    def conn_app(self):
        # 启动app
        driver = webdriver.Remote('http://localhost:4723/wd/hub', self.representation_data)
        return driver

    def lonin(self):
        driver = self.conn_app()


if __name__ == '__main__':
    Crwal_App_douyin().lonin()