"""
@File    :   javlib.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2023/2/28      zhangyu 1.0         None
"""

import requests
from bs4 import BeautifulSoup

HOME_URL = 'https://www.javlibrary.com'

HEADER = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'referer': f'{HOME_URL}/cn',
    # 'cookie': 'cf_clearance=LHhjNRmk9JzPujq2yWH4ZFQNH8R0rwUaQtlbcUh0f8-1677568118-0-160; over18=18'
}


def search_jlib(keyword):
    home_page = f'{HOME_URL}/cn/vl_searchbyid.php?keyword={keyword}'
    soup = BeautifulSoup(requests.get(url=f'{home_page}', headers=HEADER).content, 'html.parser')
    return soup


def parse_search(search_soup):
    specific_video_title = search_soup.select_one('div#video_title')
    specific_video_jacket = search_soup.select_one('div#video_jacket')
    specific_video_info = search_soup.select_one('div#video_info')
    video_list = search_soup.select('div.videothumblist div.videos div.video')
    if specific_video_title and specific_video_info:
        video_id = specific_video_info.select_one('div#video_id td.text').get_text(strip=True)
        video_href = f"{HOME_URL}{specific_video_title.select_one('a[href][rel]').get('href').strip('.')}"
        video_dmmimg = specific_video_jacket.select_one('img').get('src')
        video_libimg = specific_video_jacket.select_one('img').get('onerror')
        video_libimg = video_libimg.split('\'')[1] if len(video_libimg.split('\'')) == 3 else video_libimg
        video_actress = specific_video_info.select_one('div#video_cast span.cast a[href]').get_text(strip=True)
        print(video_id, video_href, video_dmmimg, video_libimg, video_actress)
    elif len(video_list):
        for video_div in search_soup.select('div.videothumblist div.videos div.video'):
            video_id = video_div.select_one('div.id').get_text(strip=True)
            video_href = f"{HOME_URL}/cn{video_div.select_one('a[href][title]').get('href').strip('.')}"
            video_dmmimg = video_div.select_one('img').get('src')
            video_libimg = video_div.select_one('img').get('onerror')
            video_libimg = video_libimg.split('\'')[1] if len(video_libimg.split('\'')) == 3 else video_libimg
            print(video_id, video_href, video_dmmimg, video_libimg)


if __name__ == '__main__':
    parse_search(search_jlib(''))
