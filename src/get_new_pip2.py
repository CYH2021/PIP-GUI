import re
import os
import gzip
import tarfile
import http.client
from tqdm import tqdm
from json import dump
from urllib import request
from urllib import error

# 官网源 https://pypi.org/simple/pip/
# 北外源 https://pypi.mirrors.ustc.edu.cn/simple/pip/
# 清华源 https://pypi.tuna.tsinghua.edu.cn/simple/pip/
# 阿里源 https://mirrors.aliyun.com/pypi/simple/pip/
# 豆瓣源 https://pypi.doubanio.com/simple/pip

def get_new_pip():
    # TODO: 爬取pip压缩包最新链接
    base_url = 'https://pypi.tuna.tsinghua.edu.cn/'
    new_pip_page = 'https://pypi.tuna.tsinghua.edu.cn/simple/pip/'

    # -- TODO: 获得最新的pypi的pip网页界面
    try:
        get_page_fp: http.client.HTTPResponse = request.urlopen(new_pip_page,timeout=3)
    except error.HTTPError as e:  # 检测网络问题
            return (1, e.code)
    except error.URLError as e:
            return (1, e.reason)

    page_text = get_page_fp.read().decode('utf-8')
    # -- TODO: 获取源的所有pip名称和链接
    pip_name_regex = re.compile(r'<a.*?href=\"(.*?)\".*?>(.*?)</a>')
    pip_url_and_name = pip_name_regex.findall(page_text)
    pip_versions_dict = dict()
    for url, name in pip_url_and_name:
        url = url.replace('../../', base_url)
        pip_versions_dict[name] = url

    # -- TODO: 设置并创建数据目录
    now_dir_path = os.getcwd()
    data_path = os.path.join(now_dir_path,'pip-data')
    json_file_path = os.path.join(data_path,'PIP-Versions.json')
    if not os.path.exists(data_path):
        os.mkdir(path=data_path)

    # -- TODO: 获取源的所有pip的名称和链接
    with open(json_file_path, 'w', newline='\n') as jf:
        dump(fp=jf, obj=pip_versions_dict, indent=4)  # json.dump 储存json

    # -- TODO: 获取最新的pip名称与链接
    num_pip_version_dict = dict()
    for version in pip_versions_dict.keys():
        version_regex = re.compile(r'pip-(.*?).tar.gz')
        regex_search = version_regex.search(version)
        if regex_search is not None:
            pip_version = regex_search.groups()[0]
            # print('pip_version : ', pip_version)
            version_split = pip_version.split('.')
            if len(version_split) == 2:
                version_split.append('0')
            num_pip_version = ''.join(version_split)
            # print('num_pip_version : ', num_pip_version)
            for char in num_pip_version:
                if char.isalpha():
                    num_pip_version = num_pip_version[:num_pip_version.index(char)]
            num_pip_version_dict[num_pip_version] = version
    new_pip_version_num = str(max(int(i) for i in num_pip_version_dict.keys()))
    new_pip_version:str = num_pip_version_dict[new_pip_version_num]
    new_pip_file_url:str = pip_versions_dict[new_pip_version]
    # print('new_pip_version :', new_pip_version)
    # print('new_pip_file_url :', new_pip_file_url)

    # TODO: 下载最新的pip压缩包
    gz_file_name = new_pip_version
    gz_file_path = os.path.join(data_path,gz_file_name)
    gz_file_url = new_pip_file_url
    gz_file: http.client.HTTPResponse = request.urlopen(gz_file_url)
    with open(gz_file_path, 'wb') as f:
        f.write(gz_file.read())

    # TODO: 设置解压文件路径
    gz_file_path = os.path.join(data_path, gz_file_name)
    tar_file_name = '.'.join(gz_file_name.split('.')[:-1])
    tar_file_path = os.path.join(data_path, tar_file_name)
    # 因为用file_obj读写，所以没有用上 tar_file_name

    # TODO: 解压文件
    # -- TODO: 解压gzip文件
    with gzip.open(filename=gz_file_path) as gf:
        with open(tar_file_path,'wb') as f:
            f.write(gf.read())
    # -- TODO: 解压tar文件
    with tarfile.open(name=tar_file_path) as tf:
        file_list = tf.getnames()
        pip_name = file_list[0]
        for file in tqdm(file_list,desc='解压中'):
            tf.extract(member=file,path=data_path)
    return (0,'OK')

if __name__ == '__main__':
    get_new_pip()