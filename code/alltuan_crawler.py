# -*-coding:utf-8-*-
import time
import random
import re
import tuaninfo_crawler
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Tuannum(object):

    def __init__(self):
        super(Tuannum, self).__init__()
        self.data = {
            "review_count": 0,
            "star_5": 0,
            'star_4': 0,
            'star_3': 0,
            'star_2': 0,
            'star_1': 0
        }
        self.tuannum = 0
        self.tuaninfo = ""

    def getstr(self):
        result = '    "alltuan":\n'\
            + "    {\n"+"        \"tuannum\": "+str(self.tuannum)+",\n"\
            + "        "+'"review_tuan": "'+str(self.data["review_count"])+'",\n'\
            + "        "+'"star_5": "'+str(self.data['star_5'])+'",\n'\
            + "        "+'"star_4": "'+str(self.data['star_4'])+'",\n'\
            + "        "+'"star_3": "'+str(self.data['star_3'])+'",\n'\
            + "        "+'"star_2": "'+str(self.data['star_2'])+'",\n'\
            + "        "+'"star_1": "'+str(self.data['star_1'])+'",\n'\
            + "    }\n"\
            + self.tuaninfo    # 全部团购信息
        return result


def getalltuan(shopid, driver, istuan):
    # 在店铺主页面循环获取团购url 分别调用tuaninfo_crawler获取全部团购信息
    alltuan = Tuannum()
    if istuan == 0:
        return alltuan
    url1 = "http://www.dianping.com/shop/" + str(shopid)
    driver.get(url1)
    content = driver.page_source
    temp_txt = open("../data/temp_txt.txt", "w")
    temp_txt.write(content)
    content = content.split("\n")
    linecount = -1
    for line in content:
        linecount += 1
        if line.find("class=\"tag tag-tuan\">") != -1:
            break
    needlines = content[linecount+1:]
    linecount2 = -1
    for line in needlines:
        linecount2 += 1
        if line.find("</div>") != -1 and needlines[linecount2+1] == "":
            break
        elif line.find("http://t.dianping.com/deal/") != -1:
            alltuan.tuannum += 1
            url2 = get_string(line, "href=\"", "\"")
            time.sleep(random.randint(3, 5))
            alltuan.tuaninfo += '   "tuaninfo_' + \
                str(alltuan.tuannum)+'":\n' + \
                tuaninfo_crawler.gettuaninfo(url2, driver, shopid).getstr()

    time.sleep(random.randint(3, 5))
    url3 = "http://www.dianping.com/shop/" + str(shopid) + "/review_tuangou"
    print url3
    driver.get(url3)
    content = driver.page_source
    temp_txt = open("../data/temp.txt", "w")
    temp_txt.write(content)
    content = content.split("\n")
    pat4 = "\>\([0-9]+\)\<"
    review_count = 0
    start, end = 0, 0
    for line in content:
        if line.find('<em class="col-exp">') != -1 and line.find(u"团购点评") != -1:
            line = line.decode("utf8")
            linecut = get_string(line, "团购点评", "全部点评")
            linecut = linecut.decode("utf8")
            for i in range(len(linecut)-1):
                if linecut[i] == '(':
                    start = i
                    continue
                if linecut[i] == ')':
                    end = i
                    break
            review_count = int(linecut[start+1: end])
        elif line.find('<em class="col-exp">') != -1 and line.find(u"星") != -1:
            tmp_re = re.findall(pat4, line)
            for i in range(5):
                tmp_star = re.findall("[0-9]+", tmp_re[i])
                alltuan.data["star_"+str(5-i)] = tmp_star[0]

    alltuan.data["review_count"] = review_count
    temp_txt.close()
    return alltuan


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
