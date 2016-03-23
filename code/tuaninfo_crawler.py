#-*-coding:utf-8-*-
import time
import os
import random
import re
import HTMLParser
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Tuan(object):

    """docstring for Tuan"""

    def __init__(self):
        super(Tuan, self).__init__()
        self.data = {
            'tuan-price': 0,
            'tuan-id': 0,
            'validate-date': '00-00-00',
            'use-date': "0000-00-00至0000-00-00",
            'star-rate': 0.0,
            'discount': 0.0,
            'sold': 0
        }

    def getstr(self):
        result = "	{\n"

        result = result\
            + "        "+'"tuan-id": "'+str(self.data['tuan-id'])+'",\n'\
            + "        "+'"tuan-price": "'+str(self.data['tuan-price'])+'",\n'\
            + "        "+'"validate-date": "'+str(self.data['validate-date'])+'",\n'\
            + "        "+'"use-date": "'+str(self.data['use-date'])+'",\n'\
            + "        "+'"star-rate": "'+str(self.data['star-rate'])+'",\n'\
            + "        "+'"discount": "'+str(self.data['discount'])+'",\n'\
            + "        "+'"sold": "'+str(self.data['sold'])+'",\n'
        result = result+"    }\n"
        return result


def gettuaninfo(url2, driver, shopid):

    # 根据团购url2获取团购信息
    driver.get(url2)
    content = driver.page_source
    temp_txt = open("../data/temp_txt.txt", "w")
    temp_txt.write(content)
    # begin tuaninfo source
    for i in range(1, 10):
        if os.path.exists("../source/" + str(shopid) + "_tuaninfo" + str(i) + ".txt"):
            continue
        else:
            tuaninfo_txt = open("../source/" + str(shopid) + "_tuaninfo_" + str(i) + ".txt", "w")
            tuaninfo_txt.write(content)
            tuaninfo_txt.close()
            break
    # end tuaninfo source
    content = content.split("\n")
    tuan = Tuan()
    tuan.data['tuan-id'] = get_string(url2+",", "deal/", ",")
    pat = '20[0-1][0-9]-[0-1]?[0-9]-[0-3]?[0-9]'
    pat2 = "[0-5]\.[0-9]"
    pat3 = "\>[0-9]+\<"
    # pat5="20[0-1][0-9]-[0-1][0-9]-[0-3][0-9]至20[0-1][0-9]-[0-1][0-9]-[0-3][0-9]"
    pat4 = "2014-05-19至2015-12-19"
    linecount = -1
    html_parser = HTMLParser.HTMLParser()
    for line in content:
        linecount += 1
        if line.find('<span>') != -1 and line.find(u"有效期：至") != -1:
            tmp = re.findall(pat, line)
            tuan.data['validate-date'] = tmp[0]
        elif line.find(u'>购买须知<') != -1:
            needlines = content[linecount:linecount+10]
            for needline in needlines:
                tmp = re.findall(pat, needline)
                if len(tmp) != 0:
                    tuan.data["use-date"] = tmp[0]+"至"+tmp[1]
                    break
        elif line.find('"star-rate">') != -1:
            tmp = re.findall(pat2, line)
            tuan.data["star-rate"] = tmp[0]
        elif line.find('data-eval-config') != -1 and line.find("price") != -1:
            line = line.decode("utf8")
            needline = html_parser.unescape(line)
            tuan.data["tuan-price"] = get_string(needline, '"price":', ",")
            tuan.data['discount'] = get_string(needline, '"discount":', "}")
            tuan.data["sold"] = get_string(needline, '"sold":', ",")
    time.sleep(random.randint(3, 5))
    return tuan


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
