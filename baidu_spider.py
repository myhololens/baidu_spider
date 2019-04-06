# -*- coding: utf-8 -*-
# spider_cat.py
# @author 钱弘毅
# @description 利用关键词爬取百度图片
# @created Sat Apr 06 2019 18:16:25 GMT+0800 (中国标准时间)
# @last-modified Sat Apr 06 2019 18:19:59 GMT+0800 (中国标准时间)
#

import requests
import os
import re
from tqdm import tqdm
from PIL import Image
from io import BytesIO


def get_html(url, word='猫', ip=None, pagenow=0, timeout=60):
    headers = {
        "User-Agent":
        "Mozilla/5.0(Windows NT 10.0;Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 70.0.3538.77 Safari / 537.36"
    }
    form_data = {
        'z': 9,  # 特大尺寸
        'tn': 'baiduimage',
        'word': word,
        'pn': pagenow,  # 页数
        'ie': 'utf-8',
        'oe': 'utf-8',
        'lm': -1,
        'fr': '',
        'se': '',
        'sme': '',
        'width': 0,
        'height': 0,
        'hd': 0,  # 高清
        'latest': 0,  # 最新
        'copyright': 0  # 版权
    }
    html = requests.get(url=url, params=form_data, headers=headers, proxies=ip, timeout=timeout)
    html.encoding = 'utf-8'
    return html


if __name__ == '__main__':
    keyword = input("请输入搜索关键词:")

    # url = 'https://image.baidu.com/search/index'
    # pic_urls_all = set()  # 用于存放图片url的集合, 可以自动去重
    # pagenum = 100  # 百度图片每页有30张图片, 设置爬取页数
    # for pagenow in range(pagenum):
    #     result = get_html(url=url, word=keyword, pagenow=pagenow).text
    #     patten = re.compile('"objURL":"(.*?)"')
    #     pic_urls = set(patten.findall(result, re.S))  # 先利用正则表达式找到图片url
    #     pic_urls_all = pic_urls_all.union(pic_urls)

    # # 把url保存起来
    urls_file = './urls.txt'
    # with open(urls_file, 'w') as f:
    #     for url in pic_urls_all:
    #         f.write(url + '\n')

    # print(f'共发现了{len(pic_urls_all)}张{keyword}的图片')

    os.makedirs('./img/', exist_ok=True)

    with open(urls_file, 'r') as f:
        urls = f.readlines()

    idx = 1
    for url in tqdm(urls):
        try:
            r = requests.get(url.strip(), timeout=60)
        except requests.exceptions.ConnectionError as e:
            continue
        tmpIm = BytesIO(r.content)
        im = Image.open(tmpIm)

        suffix_name = '.' + url.strip().split('.')[-1]  # 后缀名
        pic_name = './img/' + keyword + '_' + str(idx) + suffix_name

        # 只要宽比高长的图片
        if im.width > im.height:
            im.save(pic_name)
            idx += 1

    print("爬取成功")
