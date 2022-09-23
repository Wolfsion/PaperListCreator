import xml.sax
import re

from Repo import Repo
from setting import *


def finds(url: str) -> bool:
    for element in url_text:
        if url.find(element) >= 0:
            return True
    return False


def keyword_match(title: str, and_match: bool = True) -> bool:
    lower_text = title.lower()
    def func1(word, text): return text.find(word) == -1
    def func2(word, text): return text.find(word) >= 0
    check_func = func1 if and_match else func2
    for keyword in keywords:
        if check_func(keyword, lower_text):
            return not and_match
    return and_match


class MHandler(xml.sax.ContentHandler):
    def __init__(self, io: Repo):
        self.curt_tag = None
        self.title = None
        self.author = None
        self.subtext = None
        self.year = None
        self.url = None

        self.id = 1
        self.repo = io
        self.kv = {}
        self.reset()
        self.params = []
        self.batch_len = 10

    def reset(self):
        self.curt_tag = None
        self.title = None
        self.author = None
        self.subtext = None
        self.year = None
        self.url = None
        self.kv = {}

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag is not None and len(tag.strip()) > 0:
            self.curt_tag = tag

            if tag in paper_tags:
                self.reset()
                self.kv['id'] = self.id
                self.id += 1

            elif tag in sub_tags:
                self.kv['sub_tag'] = str(tag)

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'title':
            self.kv['title'] = str(self.title)

        elif tag == 'author':
            self.author = re.sub(' ', '_', str(self.author))
            if 'author' not in self.kv.keys():
                self.kv['author'] = []
                self.kv['author'].append(str(self.author))
            else:
                self.kv['author'].append(str(self.author))

        elif tag in sub_tags:
            self.kv['sub_detail'] = str(self.subtext)

        elif tag == 'url':
            self.kv['url'] = str(self.url)

        elif tag == 'year':
            self.kv['year'] = str(self.year)

        elif tag in paper_tags:
            tid = int(self.kv['id']) if 'id' in self.kv.keys() else 0
            title = self.kv['title'] if 'title' in self.kv.keys() else 'NULL'
            author = self.kv['author'] if 'author' in self.kv.keys() else 'NULL'
            author = ','.join(author) if author is not None else 'NULL'
            year = self.kv['year'] if 'year' in self.kv.keys() else 0
            url = self.kv['url'] if 'url' in self.kv.keys() else 'NULL'
            # sub_text = self.kv['sub_detail'] if 'sub_detail' in self.kv.keys() else 'NULL'

            if finds(url) and year in years and keyword_match(title):
                param = (str(tid), title, author, year, url)
                self.params.append(param)

    # 内容事件处理
    def characters(self, content):
        if self.curt_tag is None:
            pass
        elif self.curt_tag == "title":
            self.title = content.strip()
        elif self.curt_tag == "author":
            self.author = content.strip()
        elif self.curt_tag in sub_tags:
            self.subtext = content.strip()
        elif self.curt_tag == "year":
            self.year = content.strip()
        elif self.curt_tag == "url":
            self.url = content.strip()

    def endDocument(self):
        print('find %d papers' % len(self.params))
        self.repo.store(self.params)
