import json
import requests
from lxml import etree


def tag_process(tags):
    if not tags:
        return ""
    if "编程" in tags and "生活" in tags:
        return "综合"
    if "编程" in tags:
        return "技术"
    if "生活" in tags:
        return "生活"
    return "综合"


data_url = "https://github.com/timqian/chinese-independent-blogs"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0; +https://zhblogs.org/docs/bot/sync)"
}

data = requests.get(data_url, headers=headers).text

tree = etree.HTML(data)

blogs = []

datalist = tree.xpath('//markdown-accessiblity-table/table/tbody/tr')

#标签处理函数
for i, data in enumerate(datalist):
    subTag_text = data.xpath('td[4]/text()')
    subTag = [tag.strip() for tag in subTag_text[0].split(";") if tag.strip()] if subTag_text else []
    mainTag = tag_process(subTag)
    feed = data.xpath('td[1]/a/@href')
    feed_url = feed[0] if feed else ""
    blog = {
        "name": data.xpath('td[2]/text()')[0],
        "url": data.xpath('td[3]/a/text()')[0],
        "sign": "",  # 上游数据源未提供，默认空值
        "mainTag": mainTag,  # 暂时填空搁置
        "subTag": subTag,
        "feed": feed_url,
        "sitemap": "",  # 暂时填空
        "from": [data_url],
        "status": "OK",  # 上游数据源未提供，默认值
        "enabled": True,  # 默认值
        "recommen": False,  # 默认值
    }
    #打印日志
    # print(f"正在爬取第{i+1}条数据...")
    blogs.append(blog)

with open("./blogs.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(blogs, ensure_ascii=False, indent=4))
