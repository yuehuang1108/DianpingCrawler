# -*-coding:utf-8-*-
from selenium import webdriver


def validshopid(shopid, driver):
    url = "http://www.dianping.com/shop/" + str(shopid)
    driver.get(url)
    content = driver.page_source
    content = content.split("\n")
    for line in content:
        if line.find("shop-closed") != -1 or line.find("errorMessage") != -1 or line.find(u"商户已关闭") != -1:
            # print line
            return False
    return True

'''
driver = webdriver.Firefox()
if validshopid(19010968, driver):
	print "yes"
else:
	print "no"
driver.close()
'''
