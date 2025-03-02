import json
from time import sleep

import requests
from lxml import etree



data_url = "http://www.jetli.com.cn/"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0; +https://zhblogs.org/docs/bot/sync)"
}

response = requests.get(data_url, headers=headers)
response.encoding = 'gb2312' # 该数据源网页使用gb2312编码
tree = etree.HTML(response.text)

blogs = []

divs = tree.xpath("//div[@class='body']/div[@class='name']")

for div in divs[2:]:
    li_list = div.xpath("./ul/li")
    for li in li_list:
        name = li.xpath("./a/text()")[0]
        url = li.xpath("./a/@href")[0]
        blog = {
            "name": name,
            "url": url,
            "sign": "",  # 上游数据源未提供，默认空值
            "mainTag": "",  # 暂时填空搁置
            "subTag": [],
            "feed": "",
            "sitemap": "",  # 暂时填空
            "from": [data_url],
            "status": "OK",  # 上游数据源未提供，默认值
            "enabled": True,  # 默认值
            "recommen": True,  # 默认值
        }
        blogs.append(blog)


with open("./blogs.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(blogs, ensure_ascii=False, indent=4))
