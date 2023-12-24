# -*- coding: utf-8 -*-

'''
@Author   :   Corley Tang
@contact  :   cutercorleytd@gmail.com
@Github   :   https://github.com/corleytd
@Time     :   2023-12-07 21:24
@Project  :   Hands-on Crawler with Python-douban_top_movie_crawler_recursive_from_guido
递归爬取豆瓣电影Top 250——基于Python之父Guido van Rossum的实现
https://movie.douban.com/top250
'''

# 导入所需的库
import asyncio
import cgi
import logging
import re
from asyncio import Queue
from collections import namedtuple
from datetime import datetime
from urllib.parse import urlparse, urljoin, urldefrag

import aiohttp
import pymongo

# 初始化常量
logger = logging.getLogger(__name__)  # 创建日志记录器
IP_PATTERN = re.compile(r'^(([01]?\d?\d|2[0-4]\d|25[0-5]\d)\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\d)$')  # 定义IP地址正则表达式
client = pymongo.MongoClient('127.0.0.1', 27017)  # 连接MongoDB数据库
db = client.crawler
state_collection = db.douban_crawl_state
content_collection = db.douban_crawl_content


def set_logger():
    '''设置日志记录'''
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(process)d-%(threadName)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # 创建一个handler，用于写入日志文件
    file_handler = logging.FileHandler('../output/douban_top_movie_crawler.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # 创建一个handler，用于输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


set_logger()


def lenient_host(host):
    '''修复域名：宽松方式获取域名（后2段）'''
    parts = host.split('.')[-2:]
    return '.'.join(parts)


def is_redirect(response):
    '''判断请求是否是重定向'''
    return response.status in (300, 301, 302, 303, 304, 305, 306, 307, 308)


# 定义命名元组，用于记录抓取信息
CrawlState = namedtuple(
    'CrawlState',
    ['url', 'next_url', 'status', 'exception', 'size', 'content_type', 'encoding', 'num_urls', 'num_new_urls']
)


class Crawler:
    '''
    爬取主类：爬网给定根url开始的一组URL
    维护两组URL：（1）urls：已获取到的链接；（2）done：FetchStatistics的列表，已爬取过的链接。
    '''

    def __init__(self, root_urls, exclude_word=None, is_strict=True, max_redirects=2, max_tries=5, num_workers=10, *,
                 loop=None):
        '''
        初始化
        :param root_urls: 起始链接列表
        :param exclude_word: 链接中需要排除的关键词
        :param is_strict: 是否严格匹配域名
        :param max_redirects: 最大重定向次数
        :param max_tries: 最大重试次数
        :param num_workers: 最大任务数
        :param loop: 事件循环
        '''
        self.root_urls = root_urls
        self.exclude_word = exclude_word
        self.is_strict = is_strict
        self.max_redirects = max_redirects
        self.max_tries = max_tries
        self.num_workers = num_workers
        self.loop = loop or asyncio.get_event_loop()
        self.queue = Queue()  # 支持协程的队列
        self.seen_urls = set()  # 已访问过的链接，不可重复
        self.done = []  # 已爬取的链接
        self.session = None  # 异步客户端会话
        self.root_domains = set()  # 根域名集合

        for url in self.root_urls:
            parts = urlparse(url)
            host = parts.hostname
            if not host:
                continue

            # 添加链接到链接集合
            self.add_url(url)

            # 添加域名到域名集合
            if IP_PATTERN.match(host):  # 解析IP
                self.root_domains.add(host)
            else:  # 解析域名
                host = host.lower()
                if self.is_strict:
                    self.root_domains.add(host)  # 严格匹配
                else:
                    self.root_domains.add(lenient_host(host))  # 宽松匹配，只添加最后2个域名段

    def close(self):
        '''关闭连接会话'''
        self.session.close()

    def check_host(self, host):
        '''
        检查是否应该抓取host：
        只有host在根域名集合中，才会被抓取
        '''
        host = host.lower()
        if host in self.root_domains:
            return True
        if IP_PATTERN.match(host):
            return False
        if self.is_strict:
            return self._check_host_strictish(host)
        else:
            return self._check_host_lenient(host)

    def _check_host_strictish(self, host):
        '''
        严格检查host是否应该被抓取：
        以www.开头与不以www.开头认为是同一个host
        '''
        host = host[4:] if host.startswith('www.') else 'www.' + host
        return host in self.root_domains

    def _check_host_lenient(self, host):
        '''
        宽松检查host是否应该被抓取：
        只判断host本身后2段是否在root_domains集合中
        '''
        return lenient_host(host) in self.root_domains

    def record_state(self, crawl_state):
        '''记录CrawlState中的成功和失败链接状态'''
        self.done.append(crawl_state)
        state_collection.insert_one(crawl_state._asdict())

    def record_content(self, url, content):
        '''记录爬取链接何HTML内容'''
        content = {
            'url': url,
            'content': content,
            'date': datetime.now()
        }
        content_collection.insert_one(content)

    def url_allowed(self, url):
        '''判断URL是否合法'''
        if self.exclude_word and self.exclude_word in url:
            return False
        parts = urlparse(url)
        if parts.scheme not in ('http', 'https'):
            logger.debug(f'ignoring {url} because it is a non-http url')
            return False
        if not self.check_host(parts.hostname):
            logger.debug(f'ignoring {url} because it is a non-root url')
            return False
        return True

    def add_url(self, url, max_redirects=None):
        '''添加链接到队列，如果链接没被访问过'''
        if max_redirects is None:
            max_redirects = self.max_redirects
        logger.debug(f'adding {url} {max_redirects}')
        self.seen_urls.add(url)
        self.queue.put_nowait((url, max_redirects))  # 放入队列，并且不阻塞

    async def parse_links(self, response):
        '''解析响应中的链接'''
        links = set()
        content_type = None
        encoding = None
        body = await response.read()  # 异步读取响应体

        if response.status == 200:
            content_type = response.headers.get('content-type')
            params = {}
            if content_type:
                content_type, params = cgi.parse_header(content_type)
            encoding = params.get('charset', 'utf-8')

            if content_type in ('text/html', 'application/xml'):
                text = await response.text()  # 异步读取文本

                urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''', text))  # 提取页面中的链接（不包含img等标签的src链接），(?i)表示不区分大小写
                if urls:
                    logger.debug(f'found {len(urls)} distinct links in {response.url}')
                    for url in urls:
                        if 'http' not in url:  # 处理非http开头的链接
                            parts = urlparse(url)
                            if parts.query and not parts.hostname:  # 只有参数，没有域名
                                url = urljoin(str(response.url), url)
                                links.add(url)
                            else:
                                try:
                                    if ';' in url:
                                        url = url.split(';')[0]
                                    full_url = urljoin(str(response.url), url)
                                    defragmented, fragment = urldefrag(full_url)
                                    if self.url_allowed(defragmented):
                                        links.add(defragmented)
                                except:
                                    logger.warning(f'Error url: {url}')
                        else:
                            links.add(url)
        state = CrawlState(  # 记录当前CrawlState
            url=str(response.url),
            next_url=None,
            status=response.status,
            exception=None,
            size=len(body),
            content_type=content_type,
            encoding=encoding,
            num_urls=len(links),
            num_new_urls=len(links - self.seen_urls)
        )
        return state, links

    async def fetch(self, url, max_redirects):
        '''抓取1个链接'''
        num_tries = 0
        exception = None
        if self.session is None:  # 第一次抓取时创建异步会话
            self.session = aiohttp.ClientSession()
        # 重试多次抓取
        while num_tries < self.max_tries:
            try:
                response = await self.session.get(url, allow_redirects=False)  # 不允许重定向
                if num_tries > 1:
                    logger.info(f'try {num_tries} for {url} success')
                break
            except aiohttp.ClientError as client_error:
                logger.error(f'try {num_tries} for {url} raised {client_error}')
                exception = client_error
            num_tries += 1
        else:  # 循环执行结束而未提前中断，抓取尝试最大次数而失败
            logger.error(f'giving up on {url} after {num_tries} tries')
            self.record_state(
                CrawlState(
                    url=url,
                    next_url=None,
                    status=None,
                    exception=exception,
                    size=0,
                    content_type=None,
                    encoding=None,
                    num_urls=0,
                    num_new_urls=0
                )
            )
            return

        # 抓取成功，解析响应，获取重定向的url
        try:
            if is_redirect(response):  # 如果响应是重定向，则获取重定向的url
                location = response.headers['location']  # 获取重定向的url
                next_url = urljoin(url, location)
                self.record_state(
                    CrawlState(
                        url=url,
                        next_url=next_url,
                        status=response.status,
                        exception=None,
                        size=0,
                        content_type=None,
                        encoding=None,
                        num_urls=0,
                        num_new_urls=0
                    )
                )
                if next_url in self.seen_urls:  # 如果重定向的url已经被访问过，则不再抓取
                    return
                if max_redirects > 0:  # 如果还能重定向，则继续往下获取新的url
                    logger.info(f'redirected to {next_url} from {url}')
                    self.add_url(next_url, max_redirects - 1)
                else:
                    logger.error(f'redirect limit reached for {next_url} from {url}')
            else:  # 不是重定向
                try:
                    state, links = await self.parse_links(response)  # 解析获取页面中的所有链接
                    self.record_state(state)
                    for link in links.difference(self.seen_urls):  # 遍历所有链接，如果链接没被访问过，则添加到队列中
                        self.queue.put_nowait((link, self.max_redirects))
                    self.seen_urls.update(links)  # 记录已经访问过的链接
                except Exception as e:
                    logger.error(f'error parsing {url}: {e}')
        finally:
            text = await response.text()  # 异步获取响应体文本
            await response.release()  # 异步释放连接
            return text

    async def consume_queue(self):
        '''持续处理队列'''
        try:
            while self.queue:
                url, max_redirects = await self.queue.get()
                assert url in self.seen_urls, f'{url} not in self.seen_urls'
                text = await self.fetch(url, max_redirects)
                self.queue.task_done()
                logger.info(f'crawled {url}, saved to mongodb')
                self.record_content(url, text)
        except asyncio.CancelledError as e:
            logger.info(f'crawl cancelled: {e}')

    async def crawl(self):
        '''运行爬取程序，直到所有任务完成'''
        tasks = [asyncio.create_task(self.consume_queue()) for _ in range(self.num_workers)]

        await self.queue.join()  # 等待队列中的所有任务完成
        '''
        try:
            await asyncio.wait_for(self.queue.join(), timeout) # 等待队列中的所有任务完成，但不超过timeout
        except asyncio.TimeoutError:
            logger.info(f'tasks timed out after {timeout} seconds, crawling done')
        '''

        for task in tasks:  # 释放所有任务
            task.cancel()


if __name__ == '__main__':
    crawler = Crawler(
        ['https://movie.douban.com/top250', 'https://movie.douban.com/chart', 'https://movie.douban.com/annual/2022/'],
        max_redirects=10
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.crawl())
    loop.close()

    crawler.close()
    client.close()
