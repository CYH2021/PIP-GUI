#! python.exe
# -*- coding: <utf-8> -*-
import re
import os
import gzip
import tarfile
import http.client
from urllib import request


def install_pip():
    # TODO: 爬取pip压缩包最新链接
    new_pip_page = 'https://pypi.org/project/pip/#files'

    # -- TODO: 获得最新的pypi的pip网页界面
    get_page_fp: http.client.HTTPResponse = request.urlopen(new_pip_page)
    page_text = get_page_fp.read().decode('utf-8')

    # -- TODO: 获得最新的pip下载链接
    the_div_regex = re.compile(r'<\s*div\s*class\s*=\s*"card file__card"\s*>(.*)<\s*/div\s*>', re.M | re.DOTALL)
    the_div_text_list = the_div_regex.findall(page_text)
    the_div_text = ''.join(''.join(the_div_text_list[0].split('\n')).split(' '))
    the_a_regex = re.compile(r'<ahref="(.*?)">')
    file_url = the_a_regex.search(the_div_text).groups()[0]
    gz_file_name = file_url.split('/')[-1]

    # TODO: 下载pip压缩包
    gz_file: http.client.HTTPResponse = request.urlopen(file_url)
    with open(gz_file_name, 'wb') as f:
        f.write(gz_file.read())

    # TODO: 设置解压文件路径
    # tar_file_name = os.path.join(os.getcwd(), '.'.join(gz_file_name.split('.')[:-1]))
    # 因为用file_obj读写，所以没有用上 tar_file_name
    now_dir_path = os.getcwd()
    gz_file_path = os.path.join(now_dir_path, gz_file_name)
    files_dir = os.path.join(now_dir_path, '.'.join(gz_file_path.split('.')[:2]))
    files_dir_path = os.getcwd()

    # TODO: 解压文件
    with gzip.open(gz_file_path, 'rb') as gf:
        with tarfile.open(fileobj=gf) as tf:
            tf.extractall(path=files_dir_path)

    # TODO: 更新安装 pip
    # os.system(f'{self.inter_path} {files_dir}\\setup.py')


install_pip()
