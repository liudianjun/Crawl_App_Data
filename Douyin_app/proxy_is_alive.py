import requests

proxies = {'http': 'http://58.218.200.223:3299', 'https': 'http://58.218.200.223:3299'}
url = 'http://www.baidu.com'
print(requests.get(url, proxies=proxies, verify=False))

