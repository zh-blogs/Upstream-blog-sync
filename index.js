const uuid = require('uuid').v4;

const csv = `https://ghproxy.com/https://raw.githubusercontent.com/timqian/chinese-independent-blogs/master/blogs-original.csv`;
const checkAPI = `https://zhblogs.ohyee.cc/api/blogs`;
const addAPI = `https://zhblogs.ohyee.cc/api/blog`;

async function main() {
  const data = await fetch(csv).then(res => res.text());
  const lastLine = data.split('\n').pop().length > 0 ? data.split('\n').pop() : data.split('\n')[data.split('\n').length - 2];
  const blog = lastLine.split(',');
  const blogsTags = blog[3].split(';');
  const name = blog[0];
  const url = blog[1];
  const tags = blogsTags.map(tag => tag.trim());
  const repeat = await fetch(checkAPI, {
    query: {
      search: blog[0],
    }
  })
  .then(res => res.json())
  .then(res => res.data.total > 0);
  if (repeat) {
    console.log(`${blog[0]} 已存在于 zhblogs 数据库，跳过`);
    return;
  }
  await fetch(addAPI, {
    method: "PUT",
    body: {
      "token": "",
      "blog": {
          "id": uuid(),
          "name": name,
          "url": url,
          "status": "unknown",
          "tags": tags,
          "repeat": false,
          "enabled": false,
          "saveweb_id": "",
          "recommend": false
      }
  }
 })
 
 console.log(`${blog[0]} 已添加到 zhblogs 数据库`);
 return true;
}

main();