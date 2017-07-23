# _*_ coding:utf-8 _*_
# MainUsage: 计划为边爬行边扫描的脚本
import requests
import gevent
from gevent.queue import Queue
from bs4 import BeautifulSoup
from AutoSqli import AutoSqli
import argparse
import threading

# CrawlUsage: use baidu to crawl the "?id=" etc url
class Crawl():

    def __init__(self, word):
        self.word = word
        self.threads = []
        self.urls = Queue()
        self.next_page = None

    def baidu_crawl(self):
        # first crawl
        # set the next page url
        # in the end
        if self.next_page:
            r = requests.get(self.next_page)
            content = r.content
            self.urls, self.next_page = self.parse_baidu_content(content)
            return self.urls, self.next_page
        elif self.word:
            print self.word+"hah!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
            r = requests.session()
            url = "http://www.baidu.com/s?wd="+self.word
            content = r.get(url).content
            # parse the content and get the urls
            self.urls, self.next_page = self.parse_baidu_content(content)
            self.word = None
            return self.urls, self.next_page

    def parse_baidu_content(self, content):
        soup = BeautifulSoup(content, "lxml")
        containers = soup.find_all(attrs={"class": "c-showurl"})
        for container in containers:
            url = container.get('href')
            if url:
                tmpPage = requests.get(url, allow_redirects=False)
                if tmpPage.status_code == 302:
                    self.urls.put(tmpPage.headers.get("location"))
        next_page = soup.find_all(attrs={"class": "n"})
        if len(next_page)==2:
            url = "http://www.baidu.com"+next_page[1].get("href")
            self.next_page = url
        elif len(next_page)==1 and next_page[0].text==u'下一页>' :
            url = "http://www.baidu.com"+next_page[0].get("href")
            self.next_page = url
        else:
            self.next_page = None
        return self.urls, self.next_page

def run(word):
    c = Crawl(word)
    c.urls, c.next_page = c.baidu_crawl()
    while True:
        while not c.urls.empty():
            url = c.urls.get().strip()
            s = AutoSqli(url)
            t = threading.Thread(target=s.run)
            # t = gevent.spawn(s.run)
            c.threads.append(t)
            t.start()
        else:
            # gevent.joinall(c.threads)
            for t in c.threads:
                t.join()
            print c.next_page
            if c.next_page:
                c.urls, c.next_page = c.baidu_crawl()
            else:
                break

def p(url):
    print url

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-w", "--word", help="the single word that you want to crawl")
    parse.add_argument("-f", "--file", help="get the word from the file")
    args = parse.parse_args()
    # word = input("please enter the word that you want to crawl")
    if args.word:
        run(args.word)
    if args.file:
        f = open(args.file, "r")
        lines = f.readlines()
        for line in lines:
            word = str(line).strip()
            run(word)
    print "All Crawl and Done!!!!!!!!!1"
