#! /Users/sugar/.pyenv/versions/skrsugar/bin/python
"""
@File    :   main.py    
@Contact :   zhangyu@onesight.com

@Modify Time    @Author @Version    @Description
------------    ------- --------    -----------
2023/1/29       zhangyu 1.0         None
"""
import copy
import datetime
import json
import math
import os
import time
import string
import requests
import random
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from skrbt.conf import get_conf, set_conf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

HEADER = {
    # ':authority': 'skrbtju.top',
    # ':method': 'GET',
    # ':path': '/search?keyword=',
    # ':scheme': 'https',
    # 'Referer': 'https://skrbtju.top/',

    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;'
              'v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}


def skrbt(key_word, home_page=get_conf('skrbt', 'HOME_PAGE'), cookie=get_conf('skrbt', 'COOKIE')):
    HEADER.update({'referer': home_page, 'cookie': cookie})
    search_page = int(key_word.split('_')[1]) if len(key_word.split('_')) > 1 else 1
    key_word = key_word.split('_')[0]
    magnetd, offset, next_page = search(key_word=key_word, home_page=home_page, page=search_page)
    # 更新配置文件
    set_conf(group='skrbt', name='HOME_PAGE', value=home_page)
    set_conf(group='skrbt', name='COOKIE', value=cookie)

    # 继续选择
    while not (chose := input('Chose one to get magnet or type in "n/N" to next page or type in "new keyword" to search:').lower()).isdigit():
        if chose in {'n', 'N'}:
            magnetd, offset, next_page = search(key_word=key_word, home_page=home_page, magnet_dict=magnetd, page=next_page, offset=offset)
        else:
            magnetd, offset, next_page = search(key_word=chose, home_page=home_page, magnet_dict=magnetd, offset=offset)
    magnet_url = magnetd.get(chose)
    while not magnet_url:
        print('Wrone id!!!')
        magnet_url = magnetd.get(input('Chose one to get magnet:'))

    return magnet_url, home_page, magnetd


def search(key_word, home_page, magnet_dict={}, page=1, offset=0):
    soup = BeautifulSoup(requests.get(url=f'{home_page}/search?keyword={key_word}&p={page}', headers=HEADER).content, 'html.parser')
    uls, table, offset_point = soup.find_all('ul', 'list-unstyled'), PrettyTable(['id', 'name', 'size', 'time']), 0
    for i, ul in enumerate(uls):
        ahref = ul.find('a', 'rrt common-link')
        offset_point = offset + i + 1
        table.add_row([
            offset_point,
            ahref.find_all('span')[0].text if len(ahref.find_all('span')) == 1 else ahref.text,
            ul.find('li', 'rrmi').find_all('span')[0].text,
            ul.find('li', 'rrmi').find_all('span')[-1].text
        ])
        magnet_dict.update({str(offset_point): f"{home_page}{ahref.get('href')}"})
    print(table)
    return magnet_dict, offset_point, page + 1


def magnet(magnet_url, home_page=get_conf('skrbt', 'HOME_PAGE')):
    HEADER.update({'referer': f'{home_page}/search'})
    soup = BeautifulSoup(requests.get(url=magnet_url, headers=HEADER).content, 'html.parser')
    magnet_href = soup.find('a', {'id': 'magnet'}).get('href')
    os.system(f"osascript -e 'set the clipboard to \"{magnet_href}\"'")
    return magnet_href


# 通过selenium点击，模拟人操作的方式获取cookie，现已废弃
def refresh_cookie(home_page=get_conf('skrbt', 'HOME_PAGE')):
    """deprecated!!!"""
    chrome_options = webdriver.ChromeOptions()
    # 无图模式
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 设置浏览器窗口大小
    chrome_options.add_argument("--window-size=256,256")
    # 设置浏览器显示百分比(缩放级别)
    chrome_options.add_argument("--force-device-scale-factor=0.7")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(home_page)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10, 0.5)
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    input_dom = wait.until(expected_conditions.visibility_of_element_located((By.NAME, 'keyword')))
    search_button = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    print(f'==== Get [input_dom] and [search_button] success. ====')
    actions.move_to_element(input_dom).perform()
    actions.click().perform()
    actions.send_keys('ABCD').perform()
    actions.move_to_element(search_button).perform()
    actions.click().perform()
    wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print(f'==== Click search for bot challenge. ====')
    result_stats = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "small[class='result-stats']")))
    results = result_stats.text
    print(f'==== Finish bot challenge! Find {results} results. ====')
    # 获取cookie
    cookie_list = driver.get_cookies()
    cookies = "; ".join([item["name"] + "=" + item["value"] + "" for item in cookie_list])
    print(f'==== Get cookie succeed. ====')
    print(cookies)
    driver.close()
    return cookies


def get_refresh_cookie():
    start_time, token_time = math.floor(time.time() * 1000) - 10001, math.floor(time.time() * 1000)
    aywcUid = f"{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    gen_token_url = f'https://skrbtju.top/anti/recaptcha/v4/gen?aywcUid={aywcUid}&_={token_time}'
    token = json.loads(requests.get(gen_token_url).text).get('token')
    cost_time = math.floor(time.time() * 1000) - start_time
    verify_url = f'https://skrbtju.top/anti/recaptcha/v4/verify?token={token}&aywcUid={aywcUid}&costtime={cost_time}'
    verify_headers = copy.deepcopy(HEADER)
    verify_headers.update({'cookie': f'aywcUid={aywcUid}'})
    resp = requests.get(verify_url, headers=verify_headers, allow_redirects=False)
    cookies = resp.cookies
    if len(cookies):
        cookie_str = '; '.join(['='.join([cookie.name, cookie.value]) for cookie in cookies])
    else:
        chrome_options = webdriver.ChromeOptions()
        # 无图模式
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置浏览器窗口大小
        chrome_options.add_argument("--window-size=256,256")
        # 设置浏览器显示百分比(缩放级别)
        chrome_options.add_argument("--force-device-scale-factor=0.6")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(verify_url)
        cookie_list = driver.get_cookies()
        cookie_str = '; '.join(['='.join([item['name'], item['value']]) for item in cookie_list])
        driver.close()
    if len(cookie_str):
        print(f'==== Get cookie succeed. ====')
        print(cookie_str)
    else:
        print(f'==== Get cookie failed! ====')
    return cookie_str


if __name__ == '__main__':
    search_kws, magnet_dict, hpurl = {}, {}, ''
    kwstr = input('Type in key_word(required, add "_2" for page 2 directly):')
    kws = kwstr.split(',')
    if len(kws) > 0:
        if hp := input('Type in HOME_PAGE(default in skrbt.ini):'):
            search_kws.update({'home_page': hp})
        if ck := input('Type in COOKIE(default in skrbt.ini):'):
            if ck.lower() in ('r', 'refresh'):
                # ck = refresh_cookie(hp or get_conf('skrbt', 'HOME_PAGE')) # deprecated
                ck = get_refresh_cookie()
            search_kws.update({'cookie': ck})
        for kw in kws:
            if kw:
                search_kws.update({'key_word': kw})
                mgurl, hpurl, magnet_dict = skrbt(**search_kws)
                print(f'\033[1;31;40m{magnet(mgurl, hpurl)}\033[0m')
        ctn = input('Continue?(n/N or key_word or magnet_index(select again)):')
        while ctn not in ('n', 'N'):
            kws = ctn.split(',')
            if len(kws) > 0:
                if len(kws) == 1 and kws[0].isdigit() and magnet_dict and kws[0] in magnet_dict:
                    mg = magnet_dict.get(kws[0])
                    print(f'\033[1;31;40m{magnet(mg, hpurl)}\033[0m')
                else:
                    for kw in kws:
                        if kw:
                            search_kws.update({'key_word': kw})
                            mgurl, hpurl, magnet_dict = skrbt(**search_kws)
                            print(f'\033[1;31;40m{magnet(mgurl, hpurl)}\033[0m')
            else:
                print('No key_word to search!')
            ctn = input('Continue?(n/N or key_word or magnet_index(select again)):')
    else:
        print('No key_word to search!')
