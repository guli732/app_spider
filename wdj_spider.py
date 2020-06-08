import requests
from lxml import etree
import time
import re
import csv
import json


def get_category_url():
    page_url = 'https://www.wandoujia.com/category/app'
    headers = {
        'referer': 'https://www.wandoujia.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    response = requests.get(page_url, headers=headers)
    text = response.content.decode('utf8')
    html = etree.HTML(text)
    urls = html.xpath("//li[@class='parent-cate']/div/a/@href")
    return urls


def get_category2_url():
    page_url = 'https://www.wandoujia.com/category/game'
    headers = {
        'referer': 'https://www.wandoujia.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    response = requests.get(page_url, headers=headers)
    text = response.content.decode('utf8')
    html = etree.HTML(text)
    urls = html.xpath("//li[@class='parent-cate']/div/a/@href")
    return urls


def get_app_url(category_url):
    id = re.findall(r'category/(\w+)_(\w+)', category_url, re.S)
    catId = id[0][0]
    subCatId = id[0][1]
    base_url = 'https://www.wandoujia.com/wdjweb/api/category/more?catId={}&subCatId={}&page={}&ctoken=ybV4FcepvlzuaEP4kXEBBWzd'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    for i in range(1, 40):
        url = base_url.format(catId, subCatId, i)
        try:
            response = requests.get(url, headers=headers)
            text = response.content.decode('utf8')
            json_data = json.loads(text)
            msg = json_data['data']['content']
            test_html = etree.HTML(msg)
            lis = test_html.xpath("//li")
            for li in lis:
                li = etree.tostring(li, encoding='utf8').decode()
                # 包名
                try:
                    package_name = re.findall(r'data-pn="(.*?)"', li)[0]
                except:
                    package_name = ''
                print(package_name)
                # id
                try:
                    app_id = re.findall(r'data-appid="(.*?)"', li)[0]
                except:
                    app_id = ''
                print(app_id)
                # 图标
                try:
                    icon = re.findall(r'data-original="(.*?)"', li)[0]
                except:
                    icon = ''
                print(icon)
                # app名称
                try:
                    app_name = re.findall(r'title="(.*?)"', li)[0]
                except:
                    app_name = ''
                print(app_name)
                # 一级分类
                try:
                    category = re.findall(r'<a class="tag-link".*?>(.*?)</a>', li)[0]
                except:
                    category = ''
                print(category)
                # 应用描述
                try:
                    msg = re.findall(r'<div class="comment">(.*?)</div>', li)[0]
                except:
                    msg = ''
                print(msg)
                # 下载量
                try:
                    download_count = re.findall(r'install-count">(.*?)人安装</span>', li)[0]
                except:
                    download_count = ''
                print(download_count)
                # 详情页
                try:
                    url = re.findall(r'href="(.*?)"', li, re.S)[0]
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
                    }
                    response = requests.get(url, headers=headers)
                    text = response.content.decode('utf8')
                    # 开发商
                    try:
                        developers = re.findall(r'<dd><span class="dev-sites" itemprop="name">(.*?)</span>', text)[0]
                    except:
                        developers = ''
                    print(developers)
                    # 版本号
                    try:
                        version = re.findall(r'<dt>版本</dt><dd>&nbsp;(.*?)</dd>', text)[0]
                    except:
                        version = ''
                    print(version)
                    # 更新时间
                    try:
                        update_time = re.findall(r'时间: (.*?)</span>', text)[0]
                    except:
                        update_time = ''
                    print(update_time)
                    # 二级分类
                    try:
                        category_two = re.findall(r'data-track="detail-click-appTag">(.*?)</a>', text)[1]
                    except:
                        category_two = ''
                    print(category_two)
                    # 标签
                    tag = ''
                except:
                    developers = ''
                    version = ''
                    update_time = ''
                    category_two = ''
                    tag = ''
                # 创建时间
                created_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                print(created_spider_time)
                # 爬虫更新时间
                updated_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(updated_spider_time)
                data_msg = []
                data_msg.append(app_id)
                data_msg.append(app_name)
                data_msg.append(package_name)
                data_msg.append(icon)
                data_msg.append(category)
                data_msg.append(category_two)
                data_msg.append(tag)
                data_msg.append(developers)
                data_msg.append(version)
                data_msg.append(update_time)
                data_msg.append(msg)
                data_msg.append(download_count)
                data_msg.append(created_spider_time)
                data_msg.append(updated_spider_time)
                save_data(data_msg)
                print('*' * 50)
                time.sleep(0.2)
        except Exception as e:
            print(e)


def get_game_url(category_url):
    id = re.findall(r'category/(\w+)_(\w+)', category_url, re.S)
    catId = id[0][0]
    subCatId = id[0][1]
    base_url = 'https://www.wandoujia.com/wdjweb/api/category/more?catId={}&subCatId={}&page={}&ctoken=QgOJP3tmu_vTDiK7QLrIn2Eq'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    for i in range(1, 40):
        url = base_url.format(catId, subCatId, i)
        try:
            response = requests.get(url, headers=headers)
            text = response.content.decode('utf8')
            json_data = json.loads(text)
            msg = json_data['data']['content']
            test_html = etree.HTML(msg)
            lis = test_html.xpath("//li")
            for li in lis:
                li = etree.tostring(li, encoding='utf8').decode()
                # 包名
                try:
                    package_name = re.findall(r'data-pn="(.*?)"', li)[0]
                except:
                    package_name = ''
                print(package_name)
                # id
                try:
                    app_id = re.findall(r'data-appid="(.*?)"', li)[0]
                except:
                    app_id = ''
                print(app_id)
                # 图标
                try:
                    icon = re.findall(r'data-original="(.*?)"', li)[0]
                except:
                    icon = ''
                print(icon)
                # app名称
                try:
                    app_name = re.findall(r'title="(.*?)"', li)[0]
                except:
                    app_name = ''
                print(app_name)
                # 一级分类
                try:
                    category = re.findall(r'<a class="tag-link".*?>(.*?)</a>', li)[0]
                except:
                    category = ''
                print(category)
                # 应用描述
                try:
                    msg = re.findall(r'<div class="comment">(.*?)</div>', li)[0]
                except:
                    msg = ''
                print(msg)
                # 下载量
                try:
                    download_count = re.findall(r'install-count">(.*?)人安装</span>', li)[0]
                except:
                    download_count = ''
                print(download_count)
                # 详情页
                try:
                    url = re.findall(r'href="(.*?)"', li, re.S)[0]
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
                    }
                    response = requests.get(url, headers=headers)
                    text = response.content.decode('utf8')
                    # 开发商
                    try:
                        developers = re.findall(r'<dd><span class="dev-sites" itemprop="name">(.*?)</span>', text)[0]
                    except:
                        developers = ''
                    print(developers)
                    # 版本号
                    try:
                        version = re.findall(r'<dt>版本</dt><dd>&nbsp;(.*?)</dd>', text)[0]
                    except:
                        version = ''
                    print(version)
                    # 更新时间
                    try:
                        update_time = re.findall(r'时间: (.*?)</span>', text)[0]
                    except:
                        update_time = ''
                    print(update_time)
                    # 二级分类
                    try:
                        category_two = re.findall(r'data-track="detail-click-appTag">(.*?)</a>', text)[1]
                    except:
                        category_two = ''
                    print(category_two)
                    # 标签
                    tag = ''
                except:
                    developers = ''
                    version = ''
                    update_time = ''
                    category_two = ''
                    tag = ''
                # 创建时间
                created_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                print(created_spider_time)
                # 爬虫更新时间
                updated_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(updated_spider_time)
                data_msg = []
                data_msg.append(app_id)
                data_msg.append(app_name)
                data_msg.append(package_name)
                data_msg.append(icon)
                data_msg.append(category)
                data_msg.append(category_two)
                data_msg.append(tag)
                data_msg.append(developers)
                data_msg.append(version)
                data_msg.append(update_time)
                data_msg.append(msg)
                data_msg.append(download_count)
                data_msg.append(created_spider_time)
                data_msg.append(updated_spider_time)
                save_data(data_msg)
                print('*' * 50)
                time.sleep(0.2)
        except Exception as e:
            print(e)



def save_data(data_msg):
    with open('wdj_data.csv', 'a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_msg)
        fp.close()
        

def main():
    title = ['id', '应用名称', '应用包名', '应用图标', '一级分类', '二级分类', '标签', '开发商', '版本号', '更新时间', '应用描述', '下载量', '创建时间', '数据更新时间']
    save_data(title)
    # 应用
    category_urls1 = get_category_url()
    for category_url in category_urls1:
        get_app_url(category_url)
    # 游戏
    category_urls2 = get_category2_url()
    for category_url in category_urls2:
        get_game_url(category_url)


if __name__ == "__main__":
    main()