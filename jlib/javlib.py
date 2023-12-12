"""
@File    :   javlib.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2023/2/28      zhangyu 1.0         None
"""

import requests
import os
from bs4 import BeautifulSoup
import cv2
import numpy as np
from io import BytesIO

HOME_URL = 'https://www.javlibrary.com'

HEADER = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': f'{HOME_URL}/cn',
    # 'cookie': 'cf_clearance=LHhjNRmk9JzPujq2yWH4ZFQNH8R0rwUaQtlbcUh0f8-1677568118-0-160; over18=18'
}


def get_page(page_url):
    soup = BeautifulSoup(requests.get(url=f'{page_url}', headers=HEADER).content, 'html.parser')
    return soup


def save_pic_with_text(text, save_path, url):
    response = requests.get(url)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (0, 0, 255)  # 颜色
    position = (50, 50)  # 位置

    cv2.putText(img, text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.imwrite(f'{save_path}/{text}.jpg', img)


def parse_search(search_soup, save_pic=False, save_path='./screenshots'):
    rlist = []
    specific_video_title = search_soup.select_one('div#video_title')
    specific_video_jacket = search_soup.select_one('div#video_jacket')
    specific_video_info = search_soup.select_one('div#video_info')
    previewthumbs = search_soup.select_one('div.previewthumbs')
    video_list = search_soup.select('div.videothumblist div.videos div.video')
    next_href, next_href_div = None, search_soup.select_one('div.page_selector a[class="page next"]')
    if next_href_div:
        next_href = f'{HOME_URL}{next_href_div.get("href")}'
    if specific_video_title and specific_video_info:
        video_id = specific_video_info.select_one('div#video_id td.text').get_text(strip=True)
        video_href = f"{HOME_URL}{specific_video_title.select_one('a[href][rel]').get('href').strip('.')}"
        video_dmmimg = specific_video_jacket.select_one('img').get('src')
        video_libimg = specific_video_jacket.select_one('img').get('onerror')
        video_libimg = video_libimg.split('\'')[1] if len(video_libimg.split('\'')) == 3 else video_libimg
        video_actress = specific_video_info.select_one('div#video_cast span.cast a[href]').get_text(strip=True)
        actress_href = specific_video_info.select_one('div#video_cast span.cast a[href]').get('href')
        previewthumbs_ = []
        if previewthumbs:
            previewthumbs_list = previewthumbs.select('a img')
            for previewthumb in previewthumbs_list:
                pre_jpg = previewthumb.get('src')
                if pre_jpg.startswith('http') and (pre_jpg.endswith('jpg') or pre_jpg.endswith('jpeg')):
                    previewthumbs_.append(pre_jpg)

        if not actress_href.startswith(HOME_URL):
            actress_href = f'{HOME_URL}/cn/{actress_href}'
        rlist.append(
            {
                'video_id': video_id,
                'video_href': video_href,
                'video_dmmimg': video_dmmimg,
                'video_libimg': video_libimg,
                'video_actress': video_actress,
                'actress_href': actress_href,
                'previewthumbs': previewthumbs_
            }
        )

        # save preview pics
        if save_pic:
            save_pic_with_text(f'{video_id}_front', save_path, video_libimg if video_libimg.startswith('http') else video_dmmimg)
            for idx, pre_jpg in enumerate(previewthumbs_):
                save_pic_with_text(f'{video_id}_pre_{idx + 1}', save_path, pre_jpg)
            os.system('osascript /Users/sugar/PycharmProjects/skrsugar/apple_scripts/openairdrop.applescript')
        print(f'finish {video_id} href: {video_href}')
        return rlist, next_href
    elif len(video_list):
        for video_div in search_soup.select('div.videothumblist div.videos div.video'):
            video_id = video_div.select_one('div.id').get_text(strip=True)
            video_href = f"{HOME_URL}/cn{video_div.select_one('a[href][title]').get('href').strip('.')}"
            video_dmmimg = video_div.select_one('img').get('src')
            video_libimg = video_div.select_one('img').get('onerror')
            video_libimg = video_libimg.split('\'')[1] if len(video_libimg.split('\'')) == 3 else video_libimg
            rlist.append(
                {
                    'video_id': video_id,
                    'video_href': video_href,
                    'video_dmmimg': video_dmmimg,
                    'video_libimg': video_libimg,
                    'video_actress': '',
                    'actress_href': ''
                }
            )

            # save preview pics
            if save_pic:
                save_pic_with_text(video_id, save_path, video_libimg if video_libimg.startswith('http') else video_dmmimg)
            print(f'finish {video_id} href: {video_href}')
        print(f'==== finish page, next page: {next_href}')
        os.system('osascript /Users/sugar/PycharmProjects/skrsugar/apple_scripts/openairdrop.applescript')
        return rlist, next_href


def search_jlib(keyword):
    home_page = f'{HOME_URL}/cn/vl_searchbyid.php?keyword={keyword}'
    return get_page(home_page)


def search_actress_for_video(page_url):
    searchs, n = parse_search(page_url, save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')
    if len(searchs):
        actress_href, video_actress = searchs[0].get('actress_href', ''), searchs[0].get('video_actress', '')
        if not actress_href:
            if actress_video_url := searchs[0].get('video_href', ''):
                actress_video_soup = get_page(actress_video_url)
                searchs, n = parse_search(actress_video_soup, save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')
                actress_href, video_actress = searchs[0].get('actress_href', ''), searchs[0].get('video_actress', '')
        if actress_href:
            actress_soup = get_page(actress_href)
            actress_details, n = parse_search(actress_soup, save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')
            for actress_detail in actress_details:
                actress_detail['actress_href'], actress_detail['video_actress'] = actress_href, video_actress
            return actress_details, n


def search_and_save(kw):
    _, n = parse_search(search_soup=search_jlib(kw), save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')
    while n:
        _, n = parse_search(search_soup=get_page(n), save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')


def actress_and_save(kw):
    actress_vids, next_url = search_actress_for_video(search_jlib(kw))
    for actress_vid in actress_vids:
        parse_search(get_page(actress_vid['video_href']), save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')
    while next_url:
        actress_vids, next_url = search_actress_for_video(get_page(next_url))
        for actress_vid in actress_vids:
            parse_search(get_page(actress_vid['video_href']), save_pic=True, save_path='/Users/sugar/PycharmProjects/skrsugar/screenshots')


if __name__ == '__main__':
    # actress_and_save('soav-040')
    search_and_save('fiv-021')
