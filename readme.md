# 博客数据爬取与汇总项目

## 项目简介
本项目用于爬取多个博客数据源并进行数据汇总，最终提供一个去重后的完整博客数据集。各数据源的爬取脚本分别存放在对应文件夹中，汇总脚本负责整合所有数据源的数据。

## 数据源
项目支持从以下博客列表站点爬取数据：

| 数据源 | 平台标识符 | 主站链接 | 采集状态 | 推荐权重值 | 信息优先权重值 |
|--------|------------|----------|--------------|------------|--------------|
| CIB | CIB | [GitHub](https://github.com/timqian/chinese-independent-blogs) | 已采集 | 0 | RSS(3), 博客地址/名称(6) |
| 博友圈 | BoYouQuan | [官网](https://www.boyouquan.com/blogs) | 已采集 | 0 | RSS(2), 博客地址/名称(4) |
| BlogFinder | BlogFinder | [官网](https://bf.zzxworld.com/) | 已采集 | 0 | RSS(1), 博客地址/名称(1) |
| 十年之约 | ForeverBlog | [官网](https://www.foreverblog.cn/) | 等待合作回复 | 0 | 博客地址/名称(3) |
| BlogWe | BlogWe | [官网](https://blogwe.com/) | 等待合作回复 | 0 | 博客地址/名称(7) |
| BKZ | BKZ | [官网](http://www.jetli.com.cn/) | 已采集 | 1 | 博客地址/名称(2) |
| Travellings | Travellings | [官网](https://travellings.cn) | 已采集 | 0 | 博客地址/名称(5) |
| Blog114 | Blog114 | [官网](https://blog114.com/e/action/ListInfo/?classid=1) | 等待合作回复 | 0 | 博客地址/名称(8), 博客签名或介绍(1) |

## 数据结构
最终导出的数据格式如下：

```typescript
export interface Blog {
  id: number; // 成员序号，自动生成
  idx: string; // 成员唯一标识，自动生成，数据库使用
  name: string; // 博客名称，必须
  url: string; // 博客链接，必须
  sign: string; // 博客签名或介绍
  main_tag: string; // 博客主标签
  sub_tag: string[]; // 博客副标签
  feed: string[]; // 博客订阅地址
  sitemap: string; // 博客网站地图
  arch: string; // 博客架构
  link_page: string; // 博客友链页面
  join_time: Date; // 博客加入时间
  update_time: Date; // 博客编辑时间
  from: string[]; // 来源，根据爬取站点的对应来源填写
  status: string; // 站点状态，对应源查看是否有站点状态标识，无则默认"OK"
  enabled: boolean; // 审核是否通过，对应源查看是否有相应字段，无则默认 true
  recommen: boolean; // 是否推荐，根据推荐权重设置，权重为 1 则 true
}
```

## 项目结构
```
├── 数据源1/
│   ├── 爬取1.py  // 数据源1的爬取脚本
│   ├── blogs.json // 数据源1的爬取结果
│
├── 数据源2/
│   ├── 爬取2.py  
│   ├── blogs.json
│
├── ...
│
├── 汇总/
│   ├── 汇总.py  // 汇总所有数据源的脚本
│   ├── blogs_all.json // 汇总后的去重数据
│   ├── conflict_blogs.json // 数据冲突记录
│
└── README.md  // 项目说明文档
```

## 使用方法

### 1. 运行爬取脚本
在 `数据源x/` 目录下执行对应的爬取脚本，例如：
```bash
python 数据源1/爬取1.py
```
爬取结果将存储在 `数据源x/blogs.json` 文件中。

### 2. 运行数据汇总脚本
在 `汇总/` 目录下执行 `汇总.py`，整合所有 `blogs.json` 数据并去重：
```bash
python 汇总/汇总.py
```
成功执行后，生成：
- `blogs_all.json`：完整的博客数据
- `conflict_blogs.json`：如果多个数据源的博客数据冲突，则记录冲突详情

## 贡献指南
1. 发现错误或改进建议请提交 Issue。
2. 欢迎提供新的数据源或优化爬取逻辑。
3. 可提交 Pull Request 贡献代码。

## 许可证
本项目采用 MIT 许可证，详情请见 LICENSE 文件。

