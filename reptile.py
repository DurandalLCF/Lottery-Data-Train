# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 22:16:00 2019

@author: Administrator
"""

# coding=utf-8
import urllib.request as ulb
import random
import time
import xlwt
 
# 免费代理IP不能保证永久有效，如果不能用可以更新
# http://www.goubanjia.com/
proxy_list_global = [
    '113.200.214.164:9999',
    '91.205.131.102:8080',
    '39.137.77.66:8080',
    '183.181.20.94:8080',
    '119.92.91.185:8080',
    '218.60.8.83:3129'
]
 
# 收集到的常用Header
my_headers_global = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
 
 
# 获取影像数据
def get_html_data(url = 'https://www.baidu.com/',proxy_list = proxy_list_global,header_list = my_headers_global):
    # 设置暂停时间为0.1秒
    t = 0.1
    time.sleep(t)
 
    # 随机从列表中选择IP、Header
    proxy = random.choice(proxy_list)
    header = random.choice(header_list)
 
#    print("proxy =",proxy)
#    print("hearder = ",header,"\n")
 
    # 基于选择的IP构建连接
    urlhandle = ulb.ProxyHandler({'http': proxy})
    opener = ulb.build_opener(urlhandle)
    ulb.install_opener(opener)
 
    # 用urllib库链接网络图像
    response = ulb.Request(url)
 
    # 增加Header伪装成浏览器
    response.add_header('User-Agent', header)
 
    # 打开网络图像文件句柄
    try:
        fp = ulb.urlopen(response)
        html_data = fp.read()
    except ulb.HTTPError:
        print("NotFound :",url)
        html_data = "NotFound"
    except ulb.URLError:
        print("URLError :",url)
        html_data = "URLError"
        
    return html_data

def save_to_excle(data_name = [],save_data = [],file_name = 'test',file_path = '',sheet_name = 'my_worksheet',encoding='utf-8'):
    if not isinstance(data_name,list) :
        raise TypeError("Data's name is not a list.")
    list_col = len(data_name)
    
    list_row = len(save_data)
    if list_row == 0:
        raise ValueError("Data is empty.")
        
    if not isinstance(save_data[0],list) :
        raise TypeError("Data are not a matrix.")
    
    file_name = file_name + '.xlsx'
    workbook = xlwt.Workbook(encoding)
    worksheet = workbook.add_sheet(sheet_name)
    for i in  range(list_col):
        worksheet.write(0,i,data_name[i])
    
    for i in range(list_row):
        if list_col != len(save_data[i]):
            raise NameError("Data are not a matrix.")
        for j in range(list_col):
            worksheet.write(i+1,j,save_data[i][j])
            
    workbook.save(file_name)
    
if __name__ == "__main__":
    name = ['a','b']
    data = [[1,2],[5,6],[5,6]]
    save_to_excle(name,data)
