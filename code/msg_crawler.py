# -*-coding:utf-8-*-
import time
import random
import re
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Msg(object):

    def __init__(self):
        super(Msg, self).__init__()
        self.msg = []

    def getstr(self):
        result = "    " + "\"messagewall\": \n"\
            + "    " + "{\n"\
            + "        " + "\"message_numbers\": " + str(len(self.msg)) + ',\n'\
            + "        " + "\"message\": [\n"
        if len(self.msg) == 0:
            pass
        else:
            for i in range(len(self.msg)-1):
                result = result + "        {\"date\": \"" + str(self.msg[i][0]) + '\", \"user_name": \"' + str(
                    self.msg[i][1]) + '\", \"content": \"' + str(self.msg[i][2]) + '\"},\n'
            result = result + "        {\"date\": \"" + str(self.msg[len(self.msg)-1][0]) + '\", \"user_name\": \"' + str(
                self.msg[len(self.msg)-1][1]) + '\", \"content\": \"' + str(self.msg[len(self.msg)-1][2]) + '\"}\n'
        result = result + "        ]\n" + "    " + "}\n"
        return result


def getmsginfo(shopid, driver, num):

    message = Msg()
    if num == 0:
        return message
    url1 = "http://m.dianping.com/shop/"+str(shopid)+"/msgwall"
    driver.get(url1)
    content = driver.page_source
    temp_txt = open("../data/temp_txt.txt", "w")
    temp_txt.write(content)
    content = content.split("\n")

    page_count = 1
    for line in content:
        if(line.find("select-txt")) != -1:
            page_count = int(get_string(line, "<span>1/", "</span>"))

    msg_txt = open("../source/" + str(shopid) + "_msg.txt", "w")
    for page_no in range(1, page_count+1):
        time.sleep(random.randint(3, 5))
        url2 = "http://m.dianping.com/shop/" + \
            str(shopid)+"/msgwall?page="+str(page_no)
        driver.get(url2)
        content = driver.page_source
        # write source
        msg_txt.write(content)
        msg_txt.write("\n\n=========================== " + str(page_no) + "  ===========================\n\n")
        # end write
        temp_txt = open("../data/temp_txt.txt", "w")
        temp_txt.write(content)
        content = content.split("\n")
        linecount = -1
        linecount2 = -1
        linecount1 = -1
        for line in content:
            linecount += 1
            if line.find("msg-wall-details") != -1:
                break
        linecount2 = linecount
        start = linecount2+1
        c_content = ""
        c_uname = ""
        c_date = ""
        pat = "[0-1][0-9]\-[0-3][0-9] [0-2][0-9]:[0-5][0-9]"
        for line in content[start:]:
            linecount += 1
            if line.find("msg-wall-details") != -1:
                linecount1 = linecount2
                linecount2 = linecount
                for needline in content[linecount1:linecount2]:
                    if needline.find("<p>") != -1 and (needline.find("</p>") != -1 or needline.find("<img") != -1) and needline.find("<p></p>") == -1:
                        if needline.find("<img") != -1:
                            c_content = get_string(needline, "<p>", "<img")
                        else:
                            c_content = get_string(needline, "<p>", "</p>")
                    elif needline.find("role-time") != -1:
                        c_uname = get_string(needline, "<span>", "</span>")
                        tmp = re.findall(pat, needline)
                        c_date = tmp[0]
                        break
                if c_date != "":
                    message.msg.append([c_date, c_uname, c_content])
                c_content = ""
                c_date = ""
        for needline in content[linecount2+1:]:

            if needline.find("<p>") != -1 and (needline.find("</p>") != -1 or needline.find("<img") != -1)and needline.find("<p></p>") == -1:
                if needline.find("<img") != -1:
                    c_content = get_string(needline, "<p>", "<img")
                else:
                    c_content = get_string(needline, "<p>", "</p>")
            elif needline.find("role-time") != -1:
                c_uname = get_string(needline, "<span>", "</span>")
                tmp = re.findall(pat, needline)
                c_date = tmp[0]
                break
        if c_date != "":
            message.msg.append([c_date, c_uname, c_content])

    msg_txt.close()
    # end source
    temp_txt.close()
    return message


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])
