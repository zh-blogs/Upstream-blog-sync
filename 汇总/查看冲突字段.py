import json


with open('conflict_blogs.json', 'r', encoding='utf-8') as f:
    blogs = json.load(f)


values = []

for blog in blogs:
    conflict_fields = blog.get('conflict_fields', {})
    for field in conflict_fields:
        if field not in values:
            values.append(field)


for value in values:
    print(value)