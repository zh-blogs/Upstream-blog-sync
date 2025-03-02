from time import sleep
import requests
import json
import math


url = "https://www.boyouquan.com/api/blogs"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; zhblogs-sync-dev/1.0)"
}


def get_total_page():
    try:
        response_json = requests.get(url=url, headers=headers)
        response_json.raise_for_status()
        response = response_json.json()
        blogs_count = int(response["total"])
        print(f"获取到一共有{blogs_count}条数据")
        return math.ceil(blogs_count / 10)  # 向上取整
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return 0


blogs = []


def get_data(total_page):
    for pageNo in range(1, total_page + 1):
        params = {
            "pageNo": pageNo,
            "pageSize": 10
        }
        try:
            response_json = requests.get(url, params=params, headers=headers)
            response_json.raise_for_status()
            response = response_json.json()

            for i, data in enumerate(response["results"]):
                blog = {
                    "name": data["name"],
                    "url": data["address"],
                    "sign": data.get("description", ""),
                    "mainTag": "",  # 默认值
                    "subTag": [],  # 默认值
                    "feed": data["rssAddress"],
                    "sitemap": "",  # 默认空值
                    "from": ["https://www.boyouquan.com/blogs"],
                    "status": "OK",  # 默认值
                    "enabled": True,  # 默认值
                    "recommen": False,  # 默认值
                }
                print(f"正在爬取第{(pageNo - 1) * 10 + i + 1}条数据")
                blogs.append(blog)
            sleep(3)  # 延时3秒，避免过度消耗服务器资源
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            continue  # 如果请求失败，跳过该页


if __name__ == "__main__":
    total_page = get_total_page()
    if total_page == 0:
        print("无法获取总页数，程序结束。")
    else:
        print(f"获取到一共有{total_page}页数据")

        get_data(total_page)
        # 保存数据到文件
        with open("blogs.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(blogs, ensure_ascii=False, indent=4))
        print("数据爬取完成，已保存到 blogs.json")
