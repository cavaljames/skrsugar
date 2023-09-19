#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
@File    :   common.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2021/11/22      zhangyu 1.0         功能类
"""
from . import redis_util
import datetime
import requests
from bs4 import BeautifulSoup

rds = redis_util.get_redis_pool(5)


def get_html(page_link, page_encoding=None):
    r = requests.get(page_link)
    if page_encoding:
        r.encoding = page_encoding
    return r.text


def get_thumbnails(home_page, max_page):
    rds.flushdb()
    page = 1
    index = 1
    location_page = home_page
    while page <= max_page:
        if page != 1:
            location_page = f'{home_page}/page/{str(page)}'
        dhtml = get_html(location_page)
        soup = BeautifulSoup(dhtml, 'html.parser')
        anchors = soup.select('ul[id="post_container"] li div[class="post_hover"] div[class="thumbnail boxx"] a')
        for anchor in anchors:
            img = anchor.select_one('img')
            title = img['alt']
            src = f"img/thumbs/{img['src'].split('/')[-1]}"
            link = anchor['href']
            rds.hset(link, 'title', title)
            rds.hset(link, 'pic', src)
            rds.hset(link, 'index', index)
            rds.hset(link, 'time', datetime.datetime.now().strftime('%Y%m%d'))
            img_name = f'./static/{src}'
            if not os.path.exists(img_name):
                download_image(img['src'], )
            print(index, link, sep='\t\t')
            index += 1
        page += 1


def download_image(image_url, save_path):
    res = requests.get(image_url, stream=True)
    if res.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in res.iter_content(1024):
                file.write(chunk)
        print("图片下载成功！")
    else:
        print("图片下载失败！")


if __name__ == '__main__':
    from PIL import Image
    from io import BytesIO
    from numpy import *

    bit = []
    for k in rds.keys():
        d = rds.hgetall(k)
        src = d['pic']
        response = requests.get(src)
        img = Image.open(BytesIO(response.content))
        w = img.width  # 图片的宽
        h = img.height  # 图片的高
        bit.append(w/h)

    print(mean(bit))
