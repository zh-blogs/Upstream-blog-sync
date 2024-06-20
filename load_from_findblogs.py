import requests
import json
import urllib.parse
import uuid

sites = []
for i in range(1,10000000):
  d = requests.get("https://bf.zzxworld.com/api/sites/" + str(i)).json()
  sites += d["sites"]
  if not d["has_more_page"]:
    break

aaa_a = [urllib.parse.urlparse(i["url"]).netloc for i in sites]
bbb_b = [urllib.parse.urlparse(i["url"]).netloc for i in requests.get("https://zhblogs.ohyee.cc/api/blogs?size=-1").json()["data"]["blogs"]]
r = set(aaa_a) - set(bbb_b)
newlist = []
for i in sites:
  if urllib.parse.urlparse(i["url"]).netloc in r:
    newlist.append(i)

for i in newlist:
  requests.put("https://zhblogs.ohyee.cc/api/blog", data=json.dumps({"blog":{"id":str(uuid.uuid4()), "name": i["title"], "url": i["url"], "status": "unknown", "tags": [], "repeat": false, "enabled": false, "saveweb_id": "", "feed": i["rss_url"], "recommend": false}})).text
