## 抖音app数据抓取
### 从1000个分享ID开始抓取 几乎可以无限循环，本项目只抓取分享页面的用户基本信息，和部分视频数据
## 文件说明
### appium_conn_app.py 
     链接手机自动从手机app上抓取用户的抖音ID 和 分享ID 支持多台设备调试抓取
### conn_mongodb.py 
     链接mongodb数据库，数据库相关的操作都在这里了
### mitmproxy_get_short_id.py
     把获取用户粉丝的抖音ID 和 分享ID 并存到书库中
### parse_share_content.py 
     解析分享页面的内容，获取用户的详细信息，并存入到数据库
### scheduler.py 
     总调度模块
    