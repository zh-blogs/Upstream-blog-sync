import json

import requests
from lxml import etree

life_blogs_url = "https://boke.lu/shl"
no_life_blogs_url = "https://boke.lu/fshl"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0)"
}

def get_data(blogs_url, tag):
    tree = etree.HTML(requests.get(blogs_url, headers=headers).text)

    blogs = []

    datalist = tree.xpath('/html/body/main/div/div/div[2]/div')[0]

    for data in datalist:
        # url和name必有
        url = data.xpath('./a/@href')[0]
        name = data.xpath('./a/ul/li[2]/dl/dt/text()')[0]
        main_tag = tag
        try:
            sign = data.xpath('./a/ul/li[2]/dl/dd/text()')[0]
        except IndexError:
            # 上游数据源未提供，默认空值
            sign = ""

        blogs.append({
            "name": name,
            "url": url,
            "sign": sign,
            "mainTag": main_tag,
            "subTag": [],   ## 上游数据源未提供，默认空
            "feed": "",  # 上游数据源未提供，默认空
            "sitemap": "",  # 暂时填空
            "from": ["https://boke.lu"],
            "status": "OK",  # 上游数据源未提供，默认值
            "enabled": True,  # 默认值
            "recommen": True
        })

    return blogs

if __name__ == "__main__":
    all_blogs = []
    all_blogs.extend(get_data(life_blogs_url, "生活"))
    all_blogs.extend(get_data(no_life_blogs_url, "综合"))

    with open("blogs.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(all_blogs, ensure_ascii=False, indent=4))

    print(f"{len(all_blogs)}条数据已经爬取完成，已保存到 blogs.json")