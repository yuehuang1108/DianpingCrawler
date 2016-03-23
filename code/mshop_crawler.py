# -*-coding:utf-8-*-
import time
import random
import re
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# 手机页面抓平均消费加网友签到数


class Mshop(object):

    def __init__(self):
        super(Mshop, self).__init__()
        self.data = {
            'avg_cost': -1,
            'signnum': -1,
            'address': "",
            "scores": []
        }

    def getstr(self):
        result = "    " + '"mshop":'+"\n    {\n"\
            + "        "+'"average": \"'+str(self.data["avg_cost"])+"\",\n"\
            + "        "+'"signnumber": \"'+str(self.data["signnum"])+"\",\n"\
            + "        "+'"address": \"'+str(self.data["address"])+"\",\n"
        if len(self.data["scores"]) != 0:
            for i in range(len(self.data["scores"])-1):
                result = result + "        " + \
                    str(self.data["scores"][i][0]) + ":" + \
                    str(self.data["scores"][i][1]) + ',\n'
            result = result + "        \"" + str(self.data["scores"][len(self.data["scores"])-1][0]) + "\": \"" \
            		+ str(self.data["scores"][len(self.data["scores"])-1][1]) + '\",\n'
        result = result + "    " + "}\n"
        return result


def getmshopinfo(shopid, driver):
    # mobile页面获取的信息
    url1 = "http://m.dianping.com/shop/"+str(shopid)
    driver.get(url1)
    content = driver.page_source
    temp_txt = open("../data/temp_txt.txt", "w")
    temp_txt.write(content)
    # begin mshopinfo source
    mshopinfo_txt = open("../source/" + str(shopid) + "_mshopinfo.txt", "w")
    mshopinfo_txt.write(content)
    mshopinfo_txt.close()
    # end shopinfo source
    content = content.split("\n")
    mshop = Mshop()
    pat = "[0-9]+"
    conlock = 0
    linecount = -1
    cu_address = ""
    cu_item = ""
    cu_score = -1
    for line in content:
        linecount += 1
        if line.find('<span class="price">') != -1 and conlock == 0:
            tmp = re.findall(pat, line)
            if len(tmp) != 0:
                mshop.data["avg_cost"] = tmp[0]
            conlock = 1
        elif line.find(u"网友签到") != -1:
            mshop.data["signnum"] = get_string(line, "(", ")")
            break
    # crawl adress info
        elif line.find('<i class="icon-address">') != -1:
            cu_address = line[line.find("</i>")+4:]
            cu_address = cu_address+content[linecount+1].lstrip()
            mshop.data['address'] = cu_address.rstrip()
        elif line.find('<div class="desc">') != -1:
            for needline in content[linecount+1:]:
                if needline.find("</div>") == -1 and needline != "":
                    cu_item = get_string(needline, "<span>", ":")
                    cu_score = get_string(needline, ":", "</span>")
                    mshop.data["scores"].append([cu_item, cu_score])
                else:
                    break

    temp_txt.close()
    return mshop


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
