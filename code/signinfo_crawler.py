#-*-coding:utf-8-*-
import time
import random
import re
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Sign(object):

    def __init__(self):
        super(Sign, self).__init__()
        self.sign = []
        self.m_num = -1

    def getstr(self):
        result = "    " + "\"Signname\": \n"\
            + "    " + "{\n"\
            + "        " + "\"sign_numbers\": " + str(len(self.sign)) + ',\n'\
            + "        " + "\"signinfo\": [\n"
        if len(self.sign) == 0:
            pass
        else:
            for i in range(len(self.sign)-1):
                result = result + \
                    "        {\"date\": \"" + str(self.sign[i][0]) + '\", \"user_name": \"' + str(
                        self.sign[i][1]) + '\"},\n'
            result = result + "        {\"date\": \"" + str(self.sign[len(self.sign)-1][
                                                      0]) + '\", \"user_name\": \"' + str(self.sign[len(self.sign)-1][1]) + '\"}\n'
        result = result + "        ]\n" + "    " + "}\n}\n"
        return result


def getsigninfo(shopid, driver, num):
    signinfo = Sign()
    if num == 0:
        return signinfo
    url1 = "http://m.dianping.com/shop/"+str(shopid)+"/Signname"
    driver.get(url1)
    content = driver.page_source
    # begin source
    sig_txt = open("../source/" + str(shopid) + "_sig.txt", "w")
    sig_txt.write(content)
    sig_txt.close()
    # end source
    temp_txt = open("../data/temp_txt.txt", "w")
    temp_txt.write(content)
    content = content.split("\n")
    linecount, linecount1, linecount2 = -1, -1, -1
    for line in content:
        linecount += 1
        if line.find("sign-name-list") != -1:
            linecount1 = linecount+1
            break
    for line in content[linecount+1:]:
        linecount += 1
        if line.find("</ul>") != -1:
            linecount2 = linecount
            break
    needlines = content[linecount1:linecount2]
    linecount = -1
    c_uname = "null"
    c_date = "null"
    while linecount < len(needlines)-1:
        linecount += 1
        if linecount % 4 == 1:
            c_uname = get_string(needlines[linecount], "<p>", "</p>")
            c_date = get_string(needlines[linecount+1], ">", "</")
            signinfo.sign.append([c_date, c_uname])
    temp_txt.close()
    return signinfo


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
