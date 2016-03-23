# -*-coding:utf-8-*-
import time
import random
import re
import HTMLParser
import linecache
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Review(object):

    """docstring for Review"""

    def __init__(self):
        super(Review, self).__init__()
        self.reviews = []
        self.defaultreviews = []
        self.data = {
            'star_5': 0,
            'star_4': 0,
            'star_3': 0,
            'star_2': 0,
            'star_1': 0
        }

    def getstr(self):
        result = "    "+"\"all_star\":\n" + "    {\n"\
            + "        " + '"star_5": '+str(self.data['star_5'])+",\n"\
            + "        " + '"star_4": '+str(self.data['star_4'])+',\n'\
            + "        " + '"star_3": '+str(self.data['star_3'])+',\n'\
            + "        " + '"star_2": '+str(self.data['star_2'])+',\n'\
            + "        " + '"star_1": '+str(self.data['star_1'])+',\n'\
            + "    }\n"
        result = result+"    " + "\"shortreviews\": \n"\
            + "    " + "{\n"\
            + "        " + "\"review_numbers\": " + str(len(self.reviews)) + ',\n'\
            + "        " + "\"review_info\": [\n"

        if len(self.reviews) == 0:
            pass
        else:
            for i in range(len(self.reviews)-1):
                result = result + "        {\"userid\": \"" + str(self.reviews[i][0]) + '\", \"check_in\": \"' + str(
                    self.reviews[i][1]) + '\", \"content\": \"' + str(self.reviews[i][2]) + '\"},\n'
            result = result + "        {\"userid\": \"" + str(self.reviews[len(self.reviews)-1][0]) + '\", \"check_in\": \"' + str(
                self.reviews[len(self.reviews)-1][1]) + '\", \"content\": \"' + str(self.reviews[len(self.reviews)-1][2]) + '\"}\n'
        result = result + "        ]\n" + "    " + "}\n"

        result = result+"    " + "\"allreviews\": \n"\
            + "    " + "{\n"\
            + "        " + "\"default_numbers\": " + str(len(self.defaultreviews)) + ',\n'\
            + "        " + "\"default_info\": [\n"
        if len(self.defaultreviews) == 0:
            pass
        else:
            for i in range(len(self.defaultreviews)-1):
                result = result + "        {\"type\": \"" + str(self.defaultreviews[i][0])+"\",\"date\": \"" + str(self.defaultreviews[i][
                    1]) + '\", \"user_name": \"' + str(self.defaultreviews[i][2]) + '\", \"content": \"' + str(self.defaultreviews[i][3]) + '\"},\n'
            result = result + "        {\"type\": \"" + str(self.defaultreviews[len(self.defaultreviews)-1][0])+"\",\"date\": \"" + str(self.defaultreviews[len(self.defaultreviews)-1][
                1]) + '\", \"user_name\": \"' + str(self.defaultreviews[len(self.defaultreviews)-1][2]) + '\", \"content\": \"' + str(self.defaultreviews[len(self.defaultreviews)-1][3]) + '\"}\n'
        result = result + "        ]\n" + "    " + "}\n"

        return result


def getreviews(shopid, driver, num):
    # 获得签到短评和全部点评信息
    # get pages
    reviewinfo = Review()
    if num == 0:
        return reviewinfo
    url = "http://www.dianping.com/shop/" + str(shopid) + "/review_short"
    driver.get(url)
    content = driver.page_source
    content = content.split("\n")
    review_count = 0
    start, end = 0, 0
    for line in content:
        if line.find("<em class=\"col-exp\">") != -1:

            for i in range(len(line)-1, 0, -1):
                if line[i] == ')':
                    end = i
                    continue
                if line[i] == '(':
                    start = i
                    break
            review_count = int(line[start+1: end])

    page_count = review_count / 15 + 1
    # print review_count
    time.sleep(random.randint(3, 5))
    # get reviews

    #begin shortreview source
    shortreview_txt = open("../source/" + str(shopid) + "_shortreview.txt", "w")
    for page_no in range(1, page_count + 1):
        url2 = "http://www.dianping.com/shop/" + \
            str(shopid) + "/review_short?pageno=" + str(page_no)
        driver.get(url2)
        content = driver.page_source
        # write source
        shortreview_txt.write(content)
        shortreview_txt.write("\n\n=========================== " + str(page_no) + "  ===========================\n\n")
        # end write
        temp_txt = open("../data/temp.txt", "w")
        temp_txt.write(content)
        content = content.split("\n")
        linecount = 0
        for line in content:
            #      "nofollow" href				href="/member/18145024">
            if line.find("review_short_") != -1:
                needlines = linecache.getlines(
                    "../data/temp.txt")[linecount: (linecount+22)]
                #current_id = get_string(line, "href=\"/member/", "\">")
                current_id, current_time, current_content, contentline = - \
                    1, -1, "", ""

                for step in range(22):

                    if needlines[step].find("\"nofollow\"") != -1 and needlines[step].find("href=\"/member/") != -1:
                        current_line = needlines[step]
                        pat1 = "href=\"/member/[0-9]+"
                        tmp1 = re.findall(pat1, current_line)
                        pat2 = "[0-9]+"
                        tmp2 = re.findall(pat2, tmp1[0])
                        current_id = tmp2[0]
                    #		class="time"		<span class="time">15-02-15 22:03</span>
                    elif needlines[step].find("class=\"time\"") != -1:
                        current_line = needlines[step]
                        pat3 = "[0-9]+-[0-9]+-[0-9]{2,2} [0-9]+:[0-9]+"
                        tmp3 = re.findall(pat3, current_line)
                        current_time = tmp3[0]
                        #current_time = get_string(current_line, "time\">", "</span>")
                        # print get_string(line, "time\">", "</span>") + "\n"
                    elif needlines[step].find('<div class="comment-txt">') != -1:
                        p_count = 0
                        for step2 in range(step, 22):
                            if needlines[step2].find("<p>") != -1:
                                p_count += 1
                            if p_count == 2:
                                contentline = contentline+needlines[step2]
                            #	print contentline
                            if p_count == 2 and needlines[step2].find("</p>") != -1:
                                break
                        current_content = get_string(
                            contentline, "<p>", "</p>")

                current_content.replace("\n", "")
                reviewinfo.reviews.append(
                    [current_id, '20' + current_time, current_content])
                #review_info[str(current_id)] = str(current_time)
            linecount += 1
        linecache.clearcache()
        time.sleep(random.randint(3, 5))
    shortreview_txt.close()
    # end source


    # the review num of star_no
    url2 = "http://www.dianping.com/shop/" + str(shopid) + "/review_more"
    driver.get(url2)
    content = driver.page_source
    content = content.split("\n")
    pat4 = "\>\([0-9]+\)\<"
    for line in content:
        if line.find('<em class="col-exp">') != -1 and line.find(u"星") != -1:
            tmp_re = re.findall(pat4, line)
            for i in range(5):
                tmp_star = re.findall("[0-9]+", tmp_re[i])
                reviewinfo.data["star_"+str(5-i)] = tmp_star[0]

    page_count = 1
    # 获得全部点评总页数
    for line in content:
        if line.find('<em class="col-exp">') != -1 and line.find(u"全部点评") != -1:
            line = line.decode("utf8")
            linecut = get_string(line, "全部点评", "签到短评")
            linecut = linecut.decode("utf8")
            for i in range(len(linecut)-1):
                if linecut[i] == '(':
                    start = i
                    continue
                if linecut[i] == ')':
                    end = i
                    break
            review_count = int(linecut[start+1: end])
            break
    page_count = review_count / 20 + 1

    #begin shortreview source
    reviewmore_txt = open("../source/" + str(shopid) + "_reviewmore.txt", "w")
    for page_no in range(1, page_count+1):
        time.sleep(random.randint(3, 5))
        url2 = "http://www.dianping.com/shop/" + \
            str(shopid)+"/review_more?pageno="+str(page_no)
        driver.get(url2)
        content = driver.page_source
        # write source
        reviewmore_txt.write(content)
        reviewmore_txt.write("\n\n=========================== " + str(page_no) + "  ===========================\n\n")
        # end write
        temp_txt = open("../data/temp_txt.txt", "w")
        temp_txt.write(content)
        content = content.split("\n")
        linecount = -1
        linecount2 = -1
        linecount1 = -1
        for line in content:
            linecount += 1
            if line.find('<div class="pic">') != -1:
                break
        linecount2 = linecount
        start = linecount2+1
        # 点评类型
        html_parser = HTMLParser.HTMLParser()
        c_type = "default"
        c_content = ""
        c_uid = ""
        c_date = ""
        pat = "[0-1][0-9]\-[0-3][0-9]"
        for line in content[start:]:
            linecount += 1
            if line.find('<div class="pic">') != -1:
                linecount1 = linecount2
                linecount2 = linecount
                unitcount = 0
                for needline in content[linecount1:linecount2]:
                    unitcount += 1
                    if needline.find("\"nofollow\"") != -1 and needline.find("href=\"/member/") != -1:

                        c_uid = get_string(needline, 'user-id="', '"')
                    elif needline.find('<p class="comment-type">') != -1:
                        c_type = get_string(
                            needline, '<p class="comment-type">', '<')
                    elif needline.find('<div class="J_brief-cont">') != -1:
                        c_content = html_parser.unescape(
                            content[linecount1+unitcount])
                    elif needline.find('<span class="time">') != -1:
                        tmp = re.findall(pat, needline)
                        c_date = tmp[0]
                        break
                if c_date != "":
                    reviewinfo.defaultreviews.append(
                        [c_type, c_date, c_uid, c_content.lstrip()])
                c_content = ""
                c_date = ""
                c_type = "default"
        unitcount = 0
        for needline in content[linecount2+1:]:
            unitcount += 1
            if needline.find("\"nofollow\"") != -1 and needline.find("href=\"/member/") != -1:
                c_uid = get_string(needline, 'user-id="', '"')
            elif needline.find('<p class="comment-type">') != -1:
                c_type = get_string(needline, '<p class="comment-type">', '<')
            elif needline.find('<div class="J_brief-cont">') != -1:
                c_content = html_parser.unescape(
                    content[linecount2+unitcount+1])
            elif needline.find('<span class="time">') != -1:
                tmp = re.findall(pat, needline)
                c_date = tmp[0]
                break
        if c_date != "":
            reviewinfo.defaultreviews.append(
                [c_type, c_date, c_uid, c_content.lstrip()])
    reviewmore_txt.close()
    # end source
    temp_txt.close()

    # print reviewinfo.reviews
    return reviewinfo


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])

'''
driver = webdriver.Firefox()
getreviews('21992602', driver).getstr()
driver.close()
'''
