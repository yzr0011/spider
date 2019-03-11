# *_*coding:utf-8 *_*

import re
import time
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import csv
import random
import pymysql

def date(html):   #（提取网页数据）

    date = (re.findall(r'g_page_config =(.+?)g_srp_loadCss', html, re.S)[0]).strip(' ;\n')
    date = json.loads(date)
    try:
        date = date['mods']['itemlist']['data']['auctions']
        for i in date:
            try:
                title = i['title']
                title = str(title)
                title = re.sub(r'\<.*?\>', '', title).strip()
                view_price = i['view_price']
                view_sales = i['view_sales']
                nick = i['nick']
                mysql(title, view_sales, view_price, nick)
            except:continue

            # print('***标题： ' + title)
            # print('***人数： '+view_sales)
            # print('***价格： '+view_price)
    except:pass



    print('=' * 60)
    print('第%d页' % y)
    print('=' * 60)  #

def write_csv_ff1(title,view_sales,view_price,nick): #####生成表格。。。后来发现每一行都有表头，隔一行出现一次。。果断去弄数据库了。。还是数据库好一点
    #首先定义一个表头信息
    headers = ['标题','人数','价格','店铺']
    #再定义一些子数据  这里定义一个列表。再用元组将其包裹
    values = [
        (title,view_sales,view_price,nick)
    ]

    with open('tbtbttb.csv','a+',encoding='utf-8',newline='') as fp:
        ww = csv.writer(fp)
        ww.writerow(headers)
        ww.writerows(values)


def mysql(title,view_sales,view_price,nick):  ################mysql
    db = pymysql.connect(host='127.0.0.1', user='用户名', password='数据库密码', db='tbtb', port=3306, charset='utf8')
    conn = db.cursor()  # 获取指针以操作数据库
    conn.execute('set names utf8')
    t = [title,view_sales,view_price,nick]
    sql = u"INSERT INTO nvzhuang(id,title,view_sales,view_price,nick) VALUES(NULL ,%s,%s,%s,%s)"
    conn.execute(sql, t)
    db.commit()  # 提交操作
    print('插入数据成功!')
    conn.close()
    db.close()

lis = []
print('开始模拟浏览器淘宝爬取++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
while True:
    a = input('请输入需要爬取的分类(输入b结束) ：  ')
    if a == 'b':
        break
    lis.append(a)

chrom_option = webdriver.ChromeOptions()
# chrom_option.add_argument('--proxy-server=http://127.0.0.1:8080')      #########这里本来使用了mitmdump，后来发现注入啥的就没有效果
###########         mitmdump -s mitmfile.py or mitmweb -s mitmfile.py
chrom_option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(executable_path=r"C:\chromedriver\chromedriver.exe", chrome_options=chrom_option)

for li in lis:

    for i in range(0, 8888888, 44):
        url = 'https://s.taobao.com/search?q={}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s={}'.format(li,i)

        y = (int(i) / 44)+1
        driver.get(url)
        shuju = driver.page_source


        if '为确保您账户的安全及正常使用，依《网络安全法》相关要求，6月1日起会员账户需绑定手机。如您还未绑定，请尽快完成，感谢您的理解及支持'in shuju:
            driver.find_element_by_id('J_Quick2Static').click()
            driver.find_element_by_id('TPL_username_1').send_keys('淘宝账号')
            time.sleep(1)
            driver.find_element_by_id('TPL_password_1').send_keys('淘宝密码')
            time.sleep(1)
            element = driver.find_element_by_id('nc_1_n1z')
            ActionChains(driver).drag_and_drop_by_offset(element, 1000, 0).perform()
            time.sleep(2)
            driver.find_element_by_id('J_SubmitStatic').click()
            time.sleep(2)

            shuju = driver.page_source

            if '亲，小二正忙，滑动一下马上回来' in shuju:
                element = driver.find_element_by_id('nc_1_n1z')
                ActionChains(driver).drag_and_drop_by_offset(element, 2000, 0).perform()
                shuju = driver.page_source
                time.sleep(8)

            else:
                time.sleep(1)
                html = driver.page_source
                date(html)

        elif '筛选条件加的太多啦' in shuju:
                break

        elif '亲，小二正忙，滑动一下马上回来'in shuju:
            time.sleep(3)
            element = driver.find_element_by_id('nc_1_n1z')
            ActionChains(driver).drag_and_drop_by_offset(element, 2000, 0).perform()
            time.sleep(8)
            shuju = driver.page_source
            if '亲，小二正忙，滑动一下马上回来' in shuju:
                time.sleep(2)
                element = driver.find_element_by_id('nc_1_n1z')
                ActionChains(driver).drag_and_drop_by_offset(element, 2000, 0).perform()
                time.sleep(8)

            time.sleep(1)
            html = driver.page_source
            date(html)


        else:
            html = shuju
            date(html)


