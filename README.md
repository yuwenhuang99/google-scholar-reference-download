# google-scholar-reference-download
## 文件介绍
### chromedriver.exe
谷歌chrome需要的驱动，驱动版本需要与浏览器版本一致
### gs_bib.py
主程序，如果gs_bib.exe无法运行，可以尝试运行该文件，但需要安装requirements.txt中的包
### gs_bib.exe
gs_bib.py打包成的exe可执行程序,在release中下载
### logo.ico
程序的图标
### requirements.txt
gs_bib.py需要的的包
### demo.gif
演示视频
## 用途
#### 下载谷歌学术的文献引用格式和BibTex
## 使用步骤
#### 1.将想要查询的若干文献放入input.txt中，每个文献一行
#### 2.运行gs_bib.exe
#### 3.文献引用和BibTex内容在results中，共有四个.txt文件：GBT 7714、MLA、APA、bibtex
#### 4.查询异常的文献保存在log文件夹的log.txt中

## 演示视频
![image](https://github.com/yuwenhuang99/google-scholar-reference-download/blob/main/demo.gif)

## 注意事项

#### 1.注意浏览器为google chrome110.0.5481.178，其他版本可能会出错
#### 2.selenium为3.141.0,如果是4.x版本，会有warnning，但不影响使用
#### 3.chromedriver需要与浏览器版本一致，而且最好与.py放在同一目录下，也可以加入环境变量，具体google
#### 4.可以下载和自己浏览器对应版本的chromedriver.exe，然后替换该目录下的chromedriver.exe

## 免责声明
### 本工具只供学习交流使用，不作为任何盈利工具使用---hyw
