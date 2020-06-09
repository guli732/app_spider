# 应用商店爬虫
## 简介
- 通过使用requests库以及lxml解析库爬虫，爬取应用宝、小米商城、豌豆荚三个应用商店的app详细信息。
## 爬取字段
- id
- 应用名称
- 应用包名
- 应用图标
- 一级分类
- 二级分类
- 标签
- 开发商
- 版本号
- 更新时间
- 应用描述
- 下载量
- 创建时间
- 数据更新时间
## 使用方法
1. 下载该项目
2. 安装scrapy库`pip3 install requests` `pip3 install lxml`
3. 分别运行`python wdj_spider.py` `python xm_spider.py` `python yyb_spider.py`
