"""
通过抖音加密后url地址下载指定的视频文件
"""
import requests
# 视频的url
url = 'http://103.78.124.146:81/2Q2W47C7BAD6F21EF40BAF09E391A782C2CDD97F7D10_jinritoutiao_E72BBB67B5D18B47D327D12F9C314EAD69DFF055_9/v9-dy-x.ixigua.com/357cb1ba22ca74a57e4d3f4ecab75145/5cbd27fc/video/m/22085dd6091bb894f188709d1ae359381261161cdda0000088b90cc113fe/?rc=M3c3Zjg4aXdsbDMzOWkzM0ApQHRAbzdIMzk0OTszNDY1PDU3PDNAKXUpQGczdylAZnFkYnMxaDFwekApNTRkamBlYWMyMGlvXy0tLS0vc3MtbyNvIzA0LjYyLS8tLTAwLS8tLi9pOmItbyM6YDBvI2ZqZl5fdGJiXmA1Ljo%3D'
# 手机浏览器的请求头
ua = { 'Uses-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'}
# 请求体 没有这个参数一样可以下载数据
par = {

        ":authority": "aweme.snssdk.com",
        ":method": "GET",
        ":path": "/aweme/v1/play/?video_id=v0300f800000bh9up8elj9kj13d2m2u0&line=0&ratio=540p&watermark=1&media_type=4&vr_type=0&improve_bitrate=0&logo_name=aweme",
        ":scheme":"https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "upgrade-insecure-requests": 1

}
res = requests.get(url, headers=ua, params=par).content
print(res)
# 把视频数据下载到本地
with open('1.mp4', 'wb') as f:
    f.write(res)