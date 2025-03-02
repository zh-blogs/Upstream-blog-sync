import json
import requests

url = "https://api.travellings.cn/all"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0)"
}


def get_main_tag(tags: str) -> str:
    tags_set = set(tags.split(','))  # 将传入的标签字符串转换为集合，去重方便判断

    # 判断是否符合“综合”标签的条件
    if ('life' in tags_set and ('tech' in tags_set or 'go' in tags_set)) or \
            ('hybrid' in tags_set or 'normal' in tags_set):
        return '综合'

    # 判断是否符合“生活”标签的条件
    if 'life' in tags_set:
        return '生活'

    # 判断是否符合“技术”标签的条件
    if ('tech' in tags_set or 'blog' in tags_set) and 'life' not in tags_set:
        return '技术'

    # 默认返回“其他”标签
    return '其他'


def get_sub_tags(tags: str) -> list:
    tags_set = set(tags.split(','))
    # 去掉 'site','forum','blog' 标签(没啥实际意义的标签)
    tags_set.discard('site')
    tags_set.discard('forum')
    tags_set.discard('blog')

    # 返回剩下的标签列表
    return list(tags_set)


data = json.loads(requests.get(url, headers=headers).text)

blogs = []

total = int(data["total"])

for blog in data["data"]:
    blogs.append({
        "name": blog["name"],
        "url": blog["url"],
        "sign": "",  # 上游数据源未提供，默认空值
        "mainTag": get_main_tag(str(blog["tag"])),
        "subTag": get_sub_tags(str(blog["tag"])),
        "feed": "", #上游数据源未提供，默认空
        "sitemap": "",  # 暂时填空
        "from": ["https://travellings.cn"],
        "status": blog["status"],  # 上游数据源未提供，默认值
        "enabled": True,  # 默认值
        "recommen": False,  # 默认值
    })

if __name__ == "__main__":
    # 保存数据到文件或其他操作
    with open("blogs.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(blogs, ensure_ascii=False, indent=4))
    print("数据爬取完成，已保存到 blogs.json")