const axios = require('axios');

const fetch = async (url, options = {}) => {
  const { query, body, headers, timeout } = options;
  const method = options.method || 'GET';
  const params = query || {};
  const _body = options.method === 'GET' ? undefined : (body || {});
  const config = {
    method,
    url,
    params,
    body: _body,
    headers: {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
      ...headers,
    },
    timeout,
  };
  const res = await axios(config);
  return res.data;
};

const csv = `https://raw.githubusercontent.com/timqian/chinese-independent-blogs/master/blogs-original.csv`;
const checkAPI = `https://zhblogs.ohyee.cc/api/blogs`;
const addAPI = `https://zhblogs.ohyee.cc/api/blog`;

async function main() {
  const data = await fetch(csv).catch(err => {
    console.log(err);
    throw new Error("获取数据失败")
  });
  console.log("获取 chinese-independent-blogs 上游数据成功");
  const lastLine = data.split('\n').pop().length > 0 ? data.split('\n').pop() : data.split('\n')[data.split('\n').length - 2];
  if (!lastLine) throw new Error("数据为空");
  const blog = lastLine.split(',');
  const blogsTags = blog[3].split(';');
  const name = blog[0];
  const url = blog[1];
  const tags = blogsTags.map(tag => tag.trim());
  const repeat = await fetch(checkAPI, {
    query: {
      search: url,
    },
    // headers: {
    //   "x-zhblogs-verify": "chinese-independent-blogs-upstream",
    //   "user-agent": "zhblogs/1.0.0"
    // },
    timeout: 300000 // 5min
  })
  .then(res => {
    return res.data.total > 0;
  })
  .catch(err => {
    console.log(err.message);
    throw new Error(`查重 ${name} 失败`)
  });
  if (repeat) {
    console.log(`${name} 已存在于 zhblogs 数据库，跳过`);
    return;
  }
  console.log(`${name} 不存在于 zhblogs 数据库，进入添加流程`);
  await fetch(addAPI, {
    method: "PUT",
    body: {
      "token": "",
      "blog": {
          "name": name,
          "url": url,
          "status": "unknown",
          "tags": tags,
          "repeat": false,
          "enabled": false,
          "saveweb_id": "",
          "recommend": false
      }
  },
  timeout: 10000
 })
  .catch(err => {
    console.log(err);
    throw new Error(`添加 ${name} 失败 - ${err}`)
  });
 
 console.log(`${name} 已添加到 zhblogs 数据库`);
 return true;
}

main();