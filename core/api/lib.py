# -*-coding:utf-8 -*-
import re
import os
import mimetypes


def isTextFileValid(filename):
    if os.path.isfile(filename):
        mimetype, encoding = mimetypes.guess_type(filename)
        if mimetype and mimetype.startswith('text'):
            return True
        else:
            return False
    else:
        return False


def getTextFileValid(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        urls = file.read()
    res = []
    for url in urls:
        if isUrlValid(url):
            res.append(url)
    return res


def isUrlValid(url):
    tmp_url = url.strip().lower()
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if re.search(url_pattern, tmp_url):
        return True
    else:
        return False

