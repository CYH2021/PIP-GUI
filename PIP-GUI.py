# coding = utf-8
# 最后修改: 2022-11-01 CYH
import sys
import re
import os
import gzip
import ctypes
import tarfile
import http.client
import tkinter as tk
from tqdm import tqdm
from json import dump
from urllib import error
from urllib import request
from threading import Thread
import tkinter.messagebox as mbox
from tkinter import filedialog as tkf
from webbrowser import open as web_open

# 官网源 https://pypi.org/simple/
# 北外源 https://pypi.mirrors.ustc.edu.cn/simple
# 清华源 https://pypi.tuna.tsinghua.edu.cn/simple/
# 阿里源 https://mirrors.aliyun.com/pypi/simple/
# 豆瓣源 https://pypi.doubanio.com/simple/


class PIP_GUI:
    def __init__(self):
        print("\n\n请勿关闭此窗口,否则脚本无法运行\n\n")
        # 窗口设定
        self.win = tk.Tk()
        self.auto_dpi(self.win)
        self.win.geometry("380x425+940+400")
        self.win.title("镜像源安装PY包 GUI")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)

        # 设置默认值
        self.inter_path: str = sys.executable
        self.inter_path_command: str = self.inter_path + ' -m '
        self.inter_name: str = os.path.basename(self.inter_path)

        # 提示
        tk.Label(self.win, text="请输入模块/包名").pack(pady=15)

        # 输入模块名称与模块版本
        ents = tk.Frame(self.win)
        self.mkname = tk.Entry(ents, width=15)
        self.mkversion = tk.Entry(ents, width=5)
        tk.Label(ents, text="模块/包名").pack(side=tk.LEFT)
        self.mkname.pack(pady=10, side=tk.LEFT)
        tk.Label(ents, text="版本").pack(side=tk.LEFT)
        self.mkversion.pack(pady=10, side=tk.LEFT)
        ents.pack()
        tk.Label(text="不输入版本默认为最新版本").pack()

        # 输入安装解释器路径
        inter_frame = tk.Frame(self.win)
        tk.Label(inter_frame, text="安装的解释器路径:").pack(anchor=tk.SW)
        self.path_text = tk.Text(inter_frame, height=1, width=30, font=('Microsoft yahei', 10))
        self.path_text.insert(tk.END, self.inter_path)

        self.path_text.pack(side=tk.LEFT)
        tk.Button(inter_frame, text="...", command=self.re_inter_path).pack(side=tk.LEFT)
        inter_frame.pack()

        # 按钮区域
        command1 = tk.Frame(self.win)
        tk.Button(command1, text="安装", command=self.install).pack(ipadx=18, side=tk.LEFT)
        tk.Button(command1, text="卸载", command=self.uninstall).pack(ipadx=18, side=tk.LEFT)
        tk.Button(command1, text="升级", command=self.upgrade).pack(ipadx=18, side=tk.LEFT)
        tk.Button(command1, text="查看", command=self.show).pack(ipadx=18, side=tk.LEFT)
        command1.pack(side=tk.TOP)

        command2 = tk.Frame(self.win)
        tk.Button(command2, text="查看已安装的包", command=self.install_list).pack(ipadx=22, side=tk.LEFT)
        tk.Button(command2, text="查看可升级的包", command=self.upgrade_list).pack(ipadx=22, side=tk.LEFT)
        command2.pack(side=tk.TOP)

        command3 = tk.Frame(self.win)
        tk.Button(command3, text="清除命令行输出", command=self.cls).pack(ipadx=22, side=tk.LEFT)
        tk.Button(command3, text="镜像源设为默认", command=self.default).pack(ipadx=22, side=tk.LEFT)
        command3.pack(side=tk.TOP)

        
        command4 = tk.Frame(self.win)
        tk.Button(command4, text="安装最新pip (pip错误可尝试此功能)", command=self.install_pip).pack(ipadx=35, side=tk.LEFT)
        command4.pack(side=tk.TOP)

        # 消息控件
        self.msg = tk.Label(self.win, text="", foreground="Red")
        self.msg.pack(ipady=6)

        # 镜像源
        tk.Label(text="镜像来源").pack()
        mirror_station = tk.Frame(self.win)
        link1 = tk.Label(mirror_station, text="清华镜像源", foreground="blue")
        link1.pack(side=tk.LEFT)
        link2 = tk.Label(mirror_station, text="北外镜像源", foreground="blue")
        link2.pack(side=tk.LEFT)
        link3 = tk.Label(mirror_station, text="豆瓣镜像源", foreground="blue")
        link3.pack(side=tk.LEFT)
        link4 = tk.Label(mirror_station, text="阿里云镜像源", foreground="blue")
        link4.pack(side=tk.LEFT)

        mirror_station.pack(fill=tk.X, padx=20)

        # 事件绑定
        link1.bind("<Button-1>", self.web_link_tuna_tsinghua)
        link2.bind("<Button-1>", self.web_link_mirrors_ustc)
        link3.bind("<Button-1>", self.web_link_tuna_douban)
        link4.bind("<Button-1>", self.web_link_mirrors_aliyun)
        self.win.mainloop()

    def auto_dpi(self,tk_:tk.Tk):
        """
        窗口高DPI缩放适配
        :param tk_: 需要DPI缩放适配的窗口对象 [tkinter.Tk]
        """
        # 调用api设置成由应用程序缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # 调用api获得当前的缩放因子
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        # 设置缩放因子
        None if tk_ is None else tk_.tk.call('tk', 'scaling', scale_factor / 75)

    @staticmethod
    def download(path, mk: str, mode: str):
        if mode == 'upgrade':
            mode = "install --upgrade"
    
        os.system(f"{path}pip --default-timeout=100 {mode} {mk} -i https://pypi.tuna.tsinghua.edu.cn/simple ")
        os.system(f"{path}pip --default-timeout=100 {mode} {mk} -i https://pypi.mirrors.ustc.edu.cn/simple ")
        os.system(f"{path}pip --default-timeout=100 {mode} {mk} -i http://pypi.douban.com/simple/ ")
        os.system(f"{path}pip --default-timeout=100 {mode} {mk} -i http://mirrors.aliyun.com/pypi/simple/ ")
        os.system(f"{path}pip --default-timeout=500 {mode} {mk}")

    def re_inter_path(self) -> None:
        get_path = tkf.askopenfilename()
        if get_path == '':
            return None

        if not os.path.exists(os.path.dirname(get_path)):
            self.msg.config(text='解释器路径不存在')
            print('解释器路径不存在!')
            return None

        if os.path.basename(get_path) != 'python.exe':
            self.msg.config(text='文件非python解释器')
            print('文件非python解释器!')
            return None

        self.inter_path = get_path
        self.inter_path_command = self.inter_path + ' -m '
        self.inter_name = os.path.basename(self.inter_path_command)

        self.path_text.delete(1.0, tk.END)
        self.path_text.insert(tk.END, self.inter_path)

        self.msg.config(text='python解释器已修改')
        print(f'python解释器已修改 {self.inter_path}')
        self.win.update()

    def install(self) -> None:
        def install_t(self):
            mk = self.mkname.get() + " " + self.mkversion.get()
            if mk == " ":
                print("请输入要安装的模块/包名")
                self.msg.config(text="请输入要安装的模块/包名")
                return None
            self.msg.config(text='安装中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + "Installing 开始安装" + "——" * 10 + "\n")
            print("正在安装", mk)
            self.download(self.inter_path_command, mk, "install")
            print("\n" + "——" * 10 + "Install-over 安装结束" + "——" * 10)
            self.msg.config(text='安装结束')
        Thread(target=lambda: install_t(self)).start()
        return None

    def uninstall(self) -> None:
        def uninstall_t(self):
            mk = self.mkname.get()
            if mk == "":
                print("请输入要卸载的模块/包名")
                self.msg.config(text="请输入要卸载的模块/包名")
                return None
            self.msg.config(text='卸载中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + "Uninstalling 开始卸载" + "——" * 10 + "\n")
            print("正在卸载", mk)
            os.system(f"{self.inter_path_command}pip uninstall -y {mk}")
            print("\n" + "——" * 10 + "Uninstall-over 卸载结束" + "——" * 10)
            self.msg.config(text='卸载结束')
        Thread(target=lambda: uninstall_t(self)).start()
        return None

    def upgrade(self) -> None:
        def upgrade_t(self):
            mk = self.mkname.get() + " " + self.mkversion.get()
            if mk == " ":
                print("请输入要升级的模块/包名")
                self.msg.config(text="请输入要升级的模块/包名")
                return None
            self.msg.config(text='升级中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + "开始升级" + "——" * 10 + "\n")
            print("正在升级", mk)
            self.download(self.inter_path_command, mk, "upgrade")
            print("\n" + "——" * 10 + "升级结束" + "——" * 10)
            self.msg.config(text='升级结束')
        Thread(target=lambda: upgrade_t(self)).start()
        return None

    def show(self) -> None:
        def show_t(self):
            mk = self.mkname.get()
            if mk == "":
                print("请输入要查看的模块/包名")
                self.msg.config(text="请输入要查看的模块/包名")
                return None
            self.msg.config(text='加载中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + f"{mk}信息" + "——" * 10 + "\n")
            Thread(target=os.system, args=(f"{self.inter_path_command}pip show -f {mk}",)).start()
            print("\n" + "——" * 10 + "END" + "——" * 10)
            self.msg.config(text='请在命令行查看信息')
        Thread(target=lambda: show_t(self)).start()
        return None

    def install_list(self) -> None:
        def install_list_t(self):
            self.msg.config(text='加载中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + f"已安装的包" + "——" * 10 + "\n")
            os.system(f"{self.inter_path_command}pip list")
            print("\n" + "——" * 10 + "END" + "——" * 10)
            self.msg.config(text='请在命令行查看信息')
        Thread(target=lambda: install_list_t(self)).start()
        return None

    def upgrade_list(self) -> None:
        def upgrade_list_t(self):
            self.msg.config(text='加载中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + f"可升级的包" + "——" * 10 + "\n")
            os.system(f"{self.inter_path_command}pip list -o")
            print("\n" + "——" * 10 + "END" + "——" * 10)
            self.msg.config(text='请在命令行查看信息')
        Thread(target=lambda: upgrade_list_t(self)).start()
        return None

    def cls(self) -> None:
        self.win.update()
        os.system("CLS")
        self.msg.config(text='已清除命令行输出')
        return None

    def default(self) -> None:
        PipDefault(self.msg)

    def install_pip(self) -> None:
        # 官网源 https://pypi.org/simple/pip/
        # 北外源 https://pypi.mirrors.ustc.edu.cn/simple/pip/
        # 清华源 https://pypi.tuna.tsinghua.edu.cn/simple/pip/
        # 阿里源 https://mirrors.aliyun.com/pypi/simple/pip/
        # 豆瓣源 https://pypi.doubanio.com/simple/pip
        def install_pip_t(self:PIP_GUI):
            # 更新窗口显示消息
            self.msg.config(text='加载中...')
            self.win.update()
            os.system("CLS")
            print("——" * 10 + f"正在下载PIP..." + "——" * 10 + "\n")

            # TODO: 爬取pip压缩包最新链接
            base_url = 'https://pypi.tuna.tsinghua.edu.cn/'
            new_pip_page = 'https://pypi.tuna.tsinghua.edu.cn/simple/pip/'

            # -- TODO: 获得最新的pypi的pip网页界面
            try:
                get_page_fp: http.client.HTTPResponse = request.urlopen(new_pip_page,timeout=3)
            except error.HTTPError as e:  # 检测网络问题
                e_s = f'网络链接错误 {e.code}'
                print(e_s)
                self.msg.config(text=e_s)
                return (1, e.code)
            except error.URLError as e:
                e_s = f'网络链接错误 {e.reason}'
                self.msg.config(text=e_s)
                print(e_s)
                return (1, e.reason)
            else:
                self.msg.config(text='请在命令行查看信息')

            page_text = get_page_fp.read().decode('utf-8')
            # -- TODO: 获取源的所有pip名称和链接
            pip_name_regex = re.compile(r'<a.*?href=\"(.*?)\".*?>(.*?)</a>')
            pip_url_and_name = pip_name_regex.findall(page_text)
            pip_versions_dict = dict()
            for url, name in tqdm(pip_url_and_name,desc='获取源的所有pip名称和链接中'):
                url = url.replace('../../', base_url)
                pip_versions_dict[name] = url

            # -- TODO: 设置并创建数据目录
            print('设置并创建数据目录中')
            now_dir_path = os.getcwd()
            data_path = os.path.join(now_dir_path,'pip-data')
            json_file_path = os.path.join(data_path,'PIP-Versions.json')
            if not os.path.exists(data_path):
                os.mkdir(path=data_path)

            # -- TODO: 保存源的所有pip的名称和链接
            print('保存源的所有pip的名称和链接中')
            with open(json_file_path, 'w', newline='\n') as jf:
                dump(fp=jf, obj=pip_versions_dict, indent=4)  # json.dump 储存json
            print(f'保存完成 {json_file_path}')

            # -- TODO: 获取最新的pip名称与链接
            num_pip_version_dict = dict()
            for version in tqdm(pip_versions_dict.keys(),desc='获取最新的pip名称与链接中'):
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
            tar_file_name = '.'.join(gz_file_name.split('.')[:-1])
            tar_file_path = os.path.join(data_path, tar_file_name)

            # TODO: 解压文件
            # -- TODO: 解压gzip文件
            print(f'解压 {gz_file_name} 文件中...')
            with gzip.open(filename=gz_file_path) as gf:
                with open(tar_file_path,'wb') as f:
                    f.write(gf.read())
            print(f'解压完成 {tar_file_path}')
            # -- TODO: 解压tar文件
            print(f'解压 {tar_file_name}文件中...')
            with tarfile.open(name=tar_file_path) as tf:
                file_list = tf.getnames()
                pip_name = file_list[0]
                for file in tqdm(file_list,desc='解压中'):
                    tf.extract(member=file,path=data_path)
            pip_path = os.path.join(data_path,pip_name)
            setup_path = os.path.join(pip_path,'setup.py')
            print(f'解压完成 {pip_path}')

            print('安装PIP中...')
            os.chdir(path=pip_path)
            print('setup_path : ',setup_path)
            os.system(f'{self.inter_path} {setup_path} install')
            print('安装完成!')
            print("\n" + "——" * 10 + "END" + "——" * 10)
            return (0,'OK')

        Thread(target=lambda: install_pip_t(self)).start()
        return None

    # bind:
    @staticmethod
    def web_link_tuna_tsinghua(event):
        web_open("https://mirrors.tuna.tsinghua.edu.cn/help/pypi/")

    @staticmethod
    def web_link_mirrors_ustc(event):
        web_open("https://mirrors.bfsu.edu.cn/pypi/web/")

    @staticmethod
    def web_link_tuna_douban(event):
        web_open("https://www.douban.com/")

    @staticmethod
    def web_link_mirrors_aliyun(event):
        web_open("https://developer.aliyun.com/mirror/")


class PipDefault:

    def __init__(self, msd_obj: tk.Label):
        self.yn = None
        self.msd_obj = msd_obj
        self.win = tk.Tk()
        self.win.geometry("350x200+620+400")
        self.win.title("设置默认PYPI源")
        self.win.resizable(False, False)
        self.win.attributes("-topmost", True)
        tk.Label(self.win, text="请选择镜像源设置为默认PYPI源").pack()
        tk.Label(self.win, text="默认源设置后，\n在命令行窗口运行pip将用您选择的镜像源安装",
                 foreground="blue").pack()
        mirror_station1 = tk.Frame(self.win)
        mirror_station2 = tk.Frame(self.win)
        button_qh = tk.Button(mirror_station1, text="清华镜像源", command=self.def_qh)
        button_qh.pack(side=tk.LEFT)
        button_bw = tk.Button(mirror_station1, text="北外镜像源", command=self.def_bw)
        button_bw.pack(side=tk.LEFT)
        button_db = tk.Button(mirror_station2, text="豆瓣镜像源", command=self.def_db)
        button_db.pack(side=tk.LEFT)
        button_al = tk.Button(mirror_station2, text="阿里镜像源", command=self.def_al)
        button_al.pack(side=tk.LEFT)

        mirror_station1.pack(padx=20)
        mirror_station2.pack(padx=20)
        button_cz = tk.Button(self.win, text="还原为官方PYPI源", command=self.def_cz)
        button_cz.pack(side=tk.TOP, ipadx=30)

        self.win.mainloop()

    def default(self, mirror_station_name: str, link: str) -> None:
        yn = mbox.askquestion(title="PIP-GUI", message=f"是否确认将{mirror_station_name}设置为默认")
        if yn == "yes":
            print("开始设置")
            os.system(f"pip config set global.index-url {link}")
            print("设置完成")
            self.msd_obj.config(text="设置完成")
        else:
            self.msd_obj.config(text="取消设置")
        self.win.destroy()

    def def_qh(self) -> None:
        self.default("清华镜像源", "https://pypi.tuna.tsinghua.edu.cn/simple")

    def def_bw(self) -> None:
        self.default("北外镜像源", "https://pypi.mirrors.ustc.edu.cn/simple")

    def def_db(self) -> None:
        self.default("豆瓣镜像源", "http://pypi.douban.com/simple/")

    def def_al(self) -> None:
        self.default("阿里镜像源", "http://mirrors.aliyun.com/pypi/simple")

    def def_cz(self) -> None:
        self.default("官方PYPI", "https://pypi.org/simple")


if __name__ == '__main__':
    pip = PIP_GUI()  # 运行
