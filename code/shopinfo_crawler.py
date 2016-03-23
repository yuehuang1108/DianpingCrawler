#-*-coding:utf-8-*-
import time
import random
import re
from selenium import webdriver
import linecache
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Shop(object):

    """docstring for Shop"""

    def __init__(self):
        super(Shop, self).__init__()
        self.data = {
            'shopid': -1,
            'creat_time': '00-00-00',
            'creat_by': 'unknown',  # new
            'v-shop': 'n',  # yes or no
            'review_total': 0,  # 全部点评数量
            'shoptype': 'unknown',
            "shopType": -1,
            "categoryId": -1,
            "cityId": -1,
            "scores": [],
            "istuan": 0,
            'poi': "null"
        }

    def getstr(self):
        result = "{\n"\
            + "    " + "\"shopid\": \"" + str(self.data['shopid']) + "\",\n"\
            + "    " + "\"creat_time\": \"" + str(self.data['creat_time']) + "\",\n"\
            + "    " + "\"creat_by\": \"" + str(self.data['creat_by']) + "\",\n"\
            + "    " + "\"shoptype\": \"" + str(self.data['shoptype']) + "\",\n"\
            + "    " + "\"shoptypenum\": \"" + str(self.data['shopType']) + "\",\n"\
            + "    " + "\"categoryId\": \"" + str(self.data['categoryId']) + "\",\n"\
            + "    " + "\"cityId\": \"" + str(self.data['cityId']) + "\",\n"\
            + "    " + "\"is_v-shop\": \"" + str(self.data['v-shop']) + "\",\n"\
            + "    " + "\"review_total\": \"" + str(self.data['review_total']) + "\",\n"\
            + "    " + "\"istuan\": \"" + str(self.data['istuan'])+"\",\n"\
            + "    " + "\"Poi\": \"" + str(self.data['poi']) + "\",\n"\

        return result


def getshopinfo(shopid, driver):
    url = "http://www.dianping.com/shop/" + str(shopid)
    driver.get(url)
    content = driver.page_source
    temp_txt = open("../data/temp_txt.txt", "w")
    # write shopinfo source file
    shopinfo_txt = open("../source/" + str(shopid) + "_shopinfo.txt", "w")
    shopinfo_txt.write(content)
    shopinfo_txt.close()
    # end shopinfo source
    temp_txt.write(content)
    content = content.split("\n")
    shop = Shop()
    shop.data['shopid'] = shopid
    # shop.data['average_cost']=mshop_crawler.getmshopinfo(shopid,driver).getcost()
    linecount = 0
    linecount1, linecount2, c_count = 0, 0, 0
    for line in content:
        # find shoptype
        if line.find("shopType:") != -1:
            shopType = line[-3: -1]
            shop.data["shopType"] = shopType
            name = shop_type(shopType)
            shop.data['shoptype'] = name
        # find if v-shop
        elif line.find("v-shop") != -1:
            shop.data["v-shop"] = "y"
        # find review_total number
        elif line.find(u"全部点评") != -1 or line.find(u">网友点评<") != -1:
            pat1 = '\([0-9]+\)'
            tmp_re = re.findall(pat1, line)
            pat2 = '[0-9]+'
            review_more_num = re.findall(pat2, tmp_re[0])
            shop.data['review_total'] = review_more_num[0]

        elif line.find("cityId:") != -1:
            if shop.data["cityId"] == -1:
                shop.data["cityId"] = get_string(line, "cityId: ", ",")
        elif line.find("categoryId:") != -1:
            if shop.data["categoryId"] == -1:
                shop.data["categoryId"] = get_string(line, "categoryId: ", ",")
        elif line.find("class=\"tag tag-tuan\">") != -1:
            shop.data["istuan"] = 1
        # poi
        elif line.find("poi:") != -1:
            if line.find("\"")!=-1:
                Poi = get_string(line, "poi: \"", "\",")
            else:
                Poi = get_string(line, "poi: '", "'")
            shop.data["poi"] = Poi
        linecount += 1
    time.sleep(random.randint(3, 5))
    # get creat time and creat by
    url2 = "http://www.dianping.com/shop/" + str(shopid) + "/editmember"
    driver.get(url2)
    content = driver.page_source
    # begin creat source
    createinfo_txt = open("../source/" + str(shopid) + "_createinfo.txt", "w")
    createinfo_txt.write(content)
    createinfo_txt.close()
    # end creat source
    content = content.split("\n")
    pat = '[0-1][0-9]-[0-1][0-9]-[0-3][0-9]'
    for line in content:
        if line.find("<span>") != -1 and line.find("/member/") != -1:
            tmp = re.findall(pat, line)
            shop.data["creat_time"] = tmp[0]
            shop.data["creat_by"] = "user"
            break
        elif line.find(u">系统<") != -1:
            tmp = re.findall(pat, line)
            shop.data["creat_time"] = tmp[0]
            shop.data["creat_by"] = "system"
            break

    # print shop.data
    temp_txt.close()
    return shop


def shop_type(shopType):
    if shopType == '30':
        return 'entertainment'
    elif shopType == '10':
        return 'food'
    elif shopType == '60':
        return 'hotel'
    elif shopType == '55':
        return 'marriage'
    elif shopType == '50':
        return 'cosmetic'
    elif shopType == '70':
        return 'child'
    elif shopType == '20':
        return 'shopping'
    elif shopType == '45':
        return 'fitness'
    elif shopType == '25':
        return 'movie'
    elif shopType == '80':
        return 'life'
    elif shopType == '90':
        return 'home'
    elif shopType == '65':
        return 'car'
    else:
        return 'other type'


def review_category(string):
    # if string.find(u"评论") != -1:
    #   return "review_numbers", str(string[0 : -3])
    if string.find(u"人均") != -1:
        return "average_cost", str(string[3: -1])
    elif string.find(u"环境") != -1:
        return "environment", str(string[3:])
    elif string.find(u"服务") != -1:
        return "service", str(string[3:])
    else:
        return "others", -1


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
