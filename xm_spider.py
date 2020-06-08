import requests
import threading
from threading import Thread
import csv
from queue import Queue
from lxml import etree
import re
import time


gLock = threading.Lock()


class Customer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            url = self.queue.get()
            # 请求页面
            text, html = self.get_html(url)
            time.sleep(0.1)
            # 解析页面
            if text != '' and html != '':
                app_info = self.parse_page(text, html)
                # 保存数据
                gLock.acquire()
                self.save_data(app_info)
                gLock.release()
            else:
                continue

    def get_html(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        }
        try:
            response = requests.get(url, headers=headers)
            text = response.content.decode('utf8')
            html = etree.HTML(text)
            return text, html
        except Exception as e:
            print(e)
        return '', ''

    def parse_page(self, text, html):
        app_info = []
        try:
            # 应用名称
            appname = html.xpath("//div[@class='intro-titles']/h3/text()")[0]
            # print(appname)
            # id
            id = re.findall(r'appId：</li><li class="special-li">(.*?)</li>', text)[0]
            # 更新时间
            try:
                pub_time = re.findall(r'更新时间：</li><li>(.*?)</li>', text)[0]
                print(pub_time)
            except:
                pub_time = ''
            # 标签
            tag = ''
            # 应用包名
            try:
                packagename = re.findall(r'包名：</li><li class="special-li">(.*?)</li>', text)[0]
            except:
                packagename = ''
            # 应用图标
            try:
                icon_url = html.xpath("//div[@class='app-info']/img/@src")[0]
            except:
                icon_url = ''
            # 下载量
            download_count = ''
            # 一级分类
            try:
                category = html.xpath("//div[@class='intro-titles']/p[2]/text()[1]")[0]
            except:
                category = ''
            # 二级分类
            category_two = ''
            # 版本号
            try:
                version_number = re.findall(r'版本号：</li><li>(.*?)</li>', text)[0]
            except:
                version_number = ''
            # 开发商
            try:
                author_name = html.xpath("//div[@class='intro-titles']/p[1]/text()")[0]
            except:
                author_name = ''
            # 应用描述
            try:
                app_disc = html.xpath("//div[@class='app-text']/p[1]/text()")[0]
                app_disc = re.sub(r'\n| |\r', '', app_disc)
            except:
                app_disc = ''
            # 创建时间（注意更新数据时不再改动）
            spider_create = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # 数据更新时间
            up_spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            app_info.append(id)
            app_info.append(appname)
            app_info.append(packagename)
            app_info.append(icon_url)
            app_info.append(category)
            app_info.append(category_two)
            app_info.append(tag)
            app_info.append(author_name)
            app_info.append(version_number)
            app_info.append(pub_time)
            app_info.append(app_disc)
            app_info.append(download_count)
            app_info.append(spider_create)
            app_info.append(up_spider_time)
            return app_info
        except Exception as e:
            print(e)
        return app_info

    def save_data(self, app_info):
        with open('xm.csv', 'a', encoding='utf8') as fp:
            writer = csv.writer(fp)
            writer.writerow(app_info)
            fp.close()


def main():
    # 创建队列
    queue = Queue()
    # 创建初始文件
    header = ['id', '应用名称', '应用包名', '应用图标', '一级分类', '二级分类', '标签', '开发商', '版本号', '更新时间', '应用描述', '下载量', '创建时间', '数据更新时间']
    with open('xm.csv', 'a', encoding='utf8') as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        fp.close()
    # 生产者
    with open('package_name.txt', 'r') as fp:
        package_names = fp.readlines()
        fp.close()
    for package_name in package_names:
        package_name = package_name.replace('\n', '')
        url = 'http://app.mi.com/details?id={}'.format(package_name)
        queue.put(url)
    # 消费者
    for i in range(4):
        customer = Customer(queue)
        customer.start()


if __name__ == '__main__':
    main()
