# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 15:28----update 2023/3/3 16:20
# @Author  : yuwen huang
# @Email   : yuwen_huang@qq.com
# @File    : gs_bib.py
# @Software: PyCharm
import requests
from selenium import webdriver
# from selenium.webdriver.chrome.webdriver import WebDriver
import time
import os
from tqdm import tqdm
import win32api

# --------------------------------------------------------------全局变量区--------------------------------------------------------------#
# __chromedriver = './chromedriver.exe'
__all_bibtex_res = []
__cite_res_dict = {'GB/T 7714': [], 'MLA': [], 'APA': []}
__log = []
__cite_styles = __cite_res_dict.keys()


# --------------------------------------------------------------函数区--------------------------------------------------------------#

def readQueryPaper(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as f:
        papers = f.read().strip('\n')
        papers_list = list(papers.split('\n'))
    return papers_list


def startChrome():  # -> WebDriver
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 无头浏览器
    # 打开浏览器
    driver = webdriver.Chrome(options=option)
    # 访问谷歌学术
    driver.get('https://scholar.google.com/')
    # 等待页面加载完成
    time.sleep(3)
    return driver


def getResByDriver(paper_name: str, driver) -> (dict, str):
    # 找到搜索框并输入关键字
    search_box = driver.find_element_by_name('q')
    search_box.clear()  # 清除搜索框
    search_box.send_keys(paper_name)
    # 找到搜索按钮并点击
    search_button = driver.find_element_by_css_selector("button[id='gs_hdr_tsb'")
    search_button.click()
    driver.find_element_by_class_name('gs_or_cit.gs_or_btn.gs_nph').click()
    # 等待页面加载完成
    time.sleep(2)
    cite_box = driver.find_elements_by_id('gs_citt')

    cite_type = cite_box[0].find_elements_by_class_name('gs_cith')
    cite_text = cite_box[0].find_elements_by_class_name('gs_citr')
    cite_res = {}
    # 分别保存三种格式的内容，GB/T 7714|MLA|APA
    for i, j in zip(cite_type, cite_text):
        ref_style = i.text.strip()
        ref_text = j.text.strip()
        cite_res[ref_style] = ref_text
        # cite_res += (f'引用格式为:{i.text.strip()},内容如下:\n{j.text.strip()}\n')
    # 记录未查询到的引用格式
    for cite_style in __cite_styles:
        if cite_res.get(cite_style, -1) == -1:
            __log.append(f'论文{paper_name}的{cite_style}格式不存在\n')
    bib_tex = driver.find_element_by_class_name('gs_citi')
    bib_res = ''
    if bib_tex.text == 'BibTeX':
        url = bib_tex.get_attribute('href')  # bibtex的url
    try:
        bib_res = requests.get(url).text
    except:
        __log.append(f'论文{paper_name}的bibtex不存在\n')
    # 点击取消，方便重复查询
    driver.find_element_by_id('gs_cit-x').click()
    return cite_res, bib_res


def store4style(cite_res: dict, bib_res: str) -> None:  # 存储结果
    if bib_res != '':  # 要找到bib才能保存,不保存''
        __all_bibtex_res.append(bib_res + '\n')  # 保存bib，加+'\n'是为了方便直接转成字符串写入
    # 维护三个列表，分别保存结果，并写入不同文件
    for k, v in cite_res.items():
        __cite_res_dict[k].append(v + '\n')


# -----------------------------------------------文件存储区-----------------------------------------------#

def mkdir(path: str) -> None:  # 创建文件
    if not os.path.exists(path):
        os.makedirs(path)


def saveList(path: str, res: list) -> None:  # 保存内容
    with open(path, 'w', encoding='utf-8') as f:
        for l in res:
            f.write(l)
    f.close()


def saveResults(cite_res_dict: dict, all_bibtex_res: list) -> None:
    # current_date = str(datetime.now()).split()[0]
    ref_path = './results'
    log_path = './log'
    mkdir(ref_path)
    mkdir(log_path)
    for k, v in cite_res_dict.items():
        k = k.replace('/', '')
        file_path = ref_path + '/' + k + '.txt'
        saveList(file_path, v)
    bib_path = ref_path + '/bibtex.txt'
    saveList(bib_path, all_bibtex_res)
    log_path = log_path + '/log.txt'
    if __log == []:
        __log.append('没有异常错误\n')
    saveList(log_path, __log)
    print(f'所有结果保存至results文件夹下,异常结果见log文件夹')


if __name__ == '__main__':
    __input_path = './input.txt'
    __paper_list = readQueryPaper(__input_path)  # 读取待查询论文
    driver = startChrome()  # 打开浏览器
    # 批量查询文献引用
    with tqdm(total=len(__paper_list)) as pbar:
        for paper in __paper_list:
            cite_res, bib_res = getResByDriver(paper, driver)
            store4style(cite_res, bib_res)
            pbar.update(1)
    # 退出浏览器
    driver.quit()
    saveResults(__cite_res_dict, __all_bibtex_res)  # 保存结果
    time.sleep(5)
