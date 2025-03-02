from time import sleep

import requests
import json

url = "https://bf.zzxworld.com/api/sites/"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0)"
}

blogs = []


def getData(page):
    response_json = requests.get(url=url + str(page), headers=headers)
    response = json.loads(response_json.text)

    for i, data in enumerate(response["sites"]):
        blog = {
            "name": data["title"],
            "url": data["url"],
            "sign": "",  # 上游数据源未提供，默认空值
            "mainTag": "",  # 上游数据源未提供，默认空值
            "subTag": [],  # 上游数据源未提供，默认空值
            "feed": data["rss_url"],
            "sitemap": "",  # 暂时填空
            "from": ["https://bf.zzxworld.com"],
            "status": "OK",  # 上游数据源未提供，默认值
            "enabled": True,  # 默认值
            "recommen": False,  # 默认值
        }
        print(f"正在爬取第{i*page + 1}条数据...")
        blogs.append(blog)

    if response["has_more_page"]:
        sleep(3)    #添加延时缓解接口服务器压力
        print(f"检测到更多页面，正在爬取第{page + 1}页")
        getData(page + 1)


if __name__ == "__main__":
    getData(1)
    # 保存数据到文件或其他操作
    with open("blogs.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(blogs, ensure_ascii=False, indent=4))
    print("数据爬取完成，已保存到 blogs.json")
