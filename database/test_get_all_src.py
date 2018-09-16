#! /usr/bin/env python3.6

import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

def GetAbsoluteRUL(base_url, source):
    if(source.startswith('http://www.')):
        url = 'http://'+source[11:]
    elif(source.startswith('http://')):
        url = source
    elif(source.startswith('www.')):
        url = source[4:]
        url = 'http://'+url
    else:
        url = base_url+'/'+source

    return url


#-----------------Execution------------------#
if __name__ == '__main__':
    download_dir = 'download'
    base_url = 'http://pythonscraping.com'

    html = urlopen(base_url)
    bs_obj = BeautifulSoup(html, 'lxml')
    download_list = bs_obj.findAll(src=True)

    for download_ele in download_list:
        print(f'download_ele = {download_ele}')
        print(f'download_ele_src = {download_ele.attrs["src"]}')
        file_url = GetAbsoluteRUL(base_url, download_ele.attrs['src'])
        print(f'file_url = {file_url}')
