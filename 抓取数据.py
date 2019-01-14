# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 11:44:40 2018

@author: Durandal
"""

from bs4 import BeautifulSoup
import zlib
import pymysql
import reptile as pc

debug_html = True

def catch_oneday_data(term = -1):
    if term == -1:
        print("error")
        return 0
       
    url = 'https://kaijiang.500.com/shtml/gdslxq/'+str(term)+'.shtml'
    if debug_html:
        print(url)

    html_data = pc.get_html_data(url)
    html_data = zlib.decompress(html_data, 16+zlib.MAX_WBITS)
    html_data = html_data.decode('GB2312','ignore')
    if debug_html:
        print(html_data)
    
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
    
if __name__ == '__main__':
    if debug_html:
        data = catch_oneday_data(2019001)
        
    else:
        pymysql.install_as_MySQLdb()
        database = pymysql.connect("localhost","root","lcf123456","lottery",charset='utf8')
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
   
    