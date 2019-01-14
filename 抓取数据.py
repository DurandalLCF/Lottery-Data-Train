# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 11:44:40 2018

@author: Durandal
"""

from bs4 import BeautifulSoup
import zlib
import pymysql
import reptile as re
import sys
import time

debug_html = False
debug_sql = False
excle = True
sql = False

def catch_oneday_data(term = -1):
    if term == -1:
        print("error")
        return 0
       
    url = 'https://kaijiang.500.com/shtml/gdslxq/'+str(term)+'.shtml'
    print(url)
    
    html_data = re.get_html_data(url)
    if html_data == "NotFound":
        return None
    if html_data == "URLError":
        t = 1
        time.sleep(t)
        return "URLError"
    
    html_data = zlib.decompress(html_data, 16+zlib.MAX_WBITS)
    html_data = html_data.decode('GB2312','ignore')
    
    tmp = []
    tmp.append(term)
    
    soup = BeautifulSoup(html_data,'html.parser')
    data = soup.find_all('li',class_ = "ball_orange")
    
    for i in range(6):
        tmp.append(data[i].get_text())
    
    data = soup.find_all('li',class_ = "ball_blue")
    tmp.append(data[0].get_text())
    
    return tmp

def save_to_mysql(cursor,database,data = -1,term = -1):
    if data == -1:
        print('error')
        return 0
    sql = "insert into 36_choose_7 values('%s',%s,%s,%s,%s,%s,%s,%s);"%(
            data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
    
    try:
        cursor.execute(sql)
        # 提交到数据库执行
        database.commit()
        #print('success,',term)
    except:
        # 如果发生错误则回滚
        database.rollback()
        print('fail,',term)
        
def save_excle():
    name = ['term','1','2','3','4','5','6','special']
    term = [[1497,2948],[2014001,2014357],
                [2015001,2015358],[2016001,2016359],
                [2017001,2017358],[2018001,2018358],
                [2019001,2019013]]
    term_len = len(term)
    all_data = []
    not_get_trem = []
    
    for i in range(term_len):
        for j in range(term[i][0],term[i][1]+1):
            tmp = catch_oneday_data(j)
            if tmp ==  None:
                not_get_trem.append(j)
                continue
            if tmp ==  "URLError":
                j = j - 1
                continue
            all_data.append(tmp)

    print(all_data)
    print(not_get_trem)
    re.save_to_excle(name,all_data,'lottery_36_choose_7','','data')
    
if __name__ == '__main__':
    pymysql.install_as_MySQLdb()
    
    if debug_html:
        term = 2019001
        data = catch_oneday_data(term)
        if debug_sql:
            print(data)
            database = pymysql.connect("172.29.22.41","root","lcf123456","lottery",charset='utf8')
            cursor = database.cursor()
            save_to_mysql(cursor,database,data,term)
    
    if excle:
        save_excle()
        
    if sql:
        database = pymysql.connect("172.29.22.41","root","lcf123456","lottery",charset='utf8')
        cursor = database.cursor()
        
        term = [[1496,2948],[2014001,2014357],
                [2015001,2015358],[2016001,2016359],
                [2017001,2017358],[2018001,2018358]]
        term_len = len(term)
    
        for i in range(4,term_len):
            print('开始周期：',i,'\n','\n')
            for j in range(term[i][0],term[i][1]+1):
                data = catch_oneday_data(j)
                save_to_mysql(cursor,database,data,j)
            print('完成周期：',i,'\n','\n')
    
        save_to_mysql(cursor,database,data,2019008)
    
        database.close()
   
    