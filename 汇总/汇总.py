import json
import os

# 优先级配置字典
PRIORITIES = {
    # 数据源路径: {"name": 优先级, "feed": 优先级}
    "../数据源1/blogs.json": {"name": 6, "feed": 3},
    "../数据源2/blogs.json": {"name": 4, "feed": 2},
    "../数据源3/blogs.json": {"name": 1, "feed": 1},
    # "../数据源4/blogs.json": {"name": 3, "feed": 0},
    # "../数据源5/blogs.json": {"name": 7, "feed": 0},
    "../数据源6/blogs.json": {"name": 2, "feed": 0},
    "../数据源7/blogs.json": {"name": 5, "feed": 0},
    # "../数据源8/blogs.json": {"name": 8, "feed": 0},
    "../数据源9/blogs.json": {"name": 9, "feed": 9}
}


def get_priority(data_path, field):
    return PRIORITIES.get(data_path, {}).get(field, 0)


def merge_blogs(data_path, all_blogs, conflict_blogs):
    with open(data_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"文件 {data_path} 格式错误，跳过该文件")
            return

    for blog in data:
        url = blog.get("url")

        if url in all_blogs:
            existing_blog = all_blogs[url]
            conflict = False
            conflict_fields = {}

            # 处理name字段冲突
            new_name = blog.get("name")
            if new_name and existing_blog.get("name"):
                new_priority = get_priority(data_path, "name")
                existing_priority = existing_blog.get("name_priority", 0)
                if new_priority > existing_priority:
                    existing_blog["name"] = new_name
                    existing_blog["name_priority"] = new_priority
                elif new_priority == existing_priority and new_name != existing_blog["name"]:
                    conflict = True
                    conflict_fields["name"] = {
                        "existing": existing_blog["name"],
                        "new": new_name
                    }
            elif new_name and not existing_blog.get("name"):
                existing_blog["name"] = new_name
                existing_blog["name_priority"] = get_priority(data_path, "name")

            # 处理feed字段冲突
            new_feed = blog.get("feed")
            if new_feed and existing_blog.get("feed"):
                new_priority = get_priority(data_path, "feed")
                existing_priority = existing_blog.get("feed_priority", 0)
                if new_priority > existing_priority:
                    existing_blog["feed"] = new_feed
                    existing_blog["feed_priority"] = new_priority
                elif new_priority == existing_priority and new_feed != existing_blog["feed"]:
                    conflict = True
                    conflict_fields["feed"] = {
                        "existing": existing_blog["feed"],
                        "new": new_feed
                    }
            elif new_feed and not existing_blog.get("feed"):
                existing_blog["feed"] = new_feed
                existing_blog["feed_priority"] = get_priority(data_path, "feed")

            # 合并其他字段（保持原有逻辑）
            for field in ["sign", "sitemap", "enabled", "recommen"]:
                existing_value = existing_blog.get(field)
                new_value = blog.get(field)
                if not existing_value and new_value:
                    existing_blog[field] = new_value

            # 处理recommen字段
            existing_blog["recommen"] = existing_blog.get("recommen", False) or blog.get("recommen", False)

            # 处理mainTag字段
            existing_main_tag = existing_blog.get("mainTag")
            new_main_tag = blog.get("mainTag")
            if existing_main_tag and new_main_tag:
                if "生活" in [existing_main_tag, new_main_tag] and "技术" in [existing_main_tag, new_main_tag]:
                    existing_blog["mainTag"] = "综合"
                elif "其他" in [existing_main_tag, new_main_tag]:
                    existing_blog["mainTag"] = existing_main_tag if existing_main_tag != "其他" else new_main_tag
                else:
                    existing_blog["mainTag"] = existing_main_tag
            elif new_main_tag:
                existing_blog["mainTag"] = new_main_tag

            # 处理subTag字段
            existing_subtags = existing_blog.get("subTag", [])
            new_subtags = blog.get("subTag", [])
            if existing_subtags or new_subtags:
                existing_blog["subTag"] = list(set(existing_subtags + new_subtags))

            # 处理status字段
            existing_status = existing_blog.get("status")
            new_status = blog.get("status")
            if existing_status and new_status and existing_status != new_status:
                if new_status == "RUN":
                    existing_blog["status"] = "OK"
                elif new_status == "ERROR":
                    existing_blog["status"] = "ERROR"

            # 合并from字段
            existing_blog["from"] = list(set(existing_blog.get("from", []) + blog.get("from", [])))

            if conflict:
                conflict_entry = next((item for item in conflict_blogs if item["url"] == url), None)
                if not conflict_entry:
                    conflict_blogs.append({
                        "url": url,
                        "existing_data": existing_blog,
                        "new_data": blog,
                        "conflict_fields": conflict_fields
                    })
        else:
            blog["name_priority"] = get_priority(data_path, "name")
            blog["feed_priority"] = get_priority(data_path, "feed")
            all_blogs[url] = blog


def save_blogs(blog_path, all_blogs, conflict_blogs):
    # 删除临时使用的优先级字段
    for blog in all_blogs.values():
        blog.pop("name_priority", None)
        blog.pop("feed_priority", None)

    with open(blog_path, "w", encoding="utf-8") as f:
        json.dump(list(all_blogs.values()), f, ensure_ascii=False, indent=4)

    if conflict_blogs:
        with open("conflict_blogs.json", "w", encoding="utf-8") as f:
            json.dump(conflict_blogs, f, ensure_ascii=False, indent=4)


def append_blogs(blog_path):
    all_blogs = {}
    conflict_blogs = []
    total_processed = 0

    # 获取所有配置的数据源路径
    data_paths = PRIORITIES.keys()

    # 验证数据源文件是否存在
    valid_paths = [path for path in data_paths if os.path.exists(path)]

    if not valid_paths:
        print("未找到有效的数据源文件")
        return

    for data_path in valid_paths:
        with open(data_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                total_processed += len(data)
                print(f"正在处理数据源: {data_path}")
            except json.JSONDecodeError:
                print(f"文件 {data_path} 格式错误，跳过该文件")
                continue
        merge_blogs(data_path, all_blogs, conflict_blogs)

    save_blogs(blog_path, all_blogs, conflict_blogs)

    print("\n合并统计信息：")
    print(f"总共处理了 {total_processed} 条数据")
    print(f"成功合并了 {len(all_blogs)} 条数据")
    print(f"发现 {len(conflict_blogs)} 条数据存在冲突，已保存至 conflict_blogs.json")
    if conflict_blogs:
        print("请检查 conflict_blogs.json 文件并手动处理冲突数据")


if __name__ == "__main__":
    blog_path = "./blogs_all.json"
    append_blogs(blog_path)