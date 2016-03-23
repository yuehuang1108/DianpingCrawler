# -*-coding:utf-8-*-
import time
import random
import validshopid
import shopinfo_crawler
import reviewinfo_crawler
import tuaninfo_crawler
import msg_crawler
import signinfo_crawler
import traceback
import alltuan_crawler
import mshop_crawler
from selenium import webdriver
import sys
sys.setdefaultencoding("utf-8")


def getshopinfo(steps):
    driver = webdriver.Firefox()
    for step in range(steps):
        try:
            shopid = random.randint(500102, 21604280)
            # shopid = 16961866
            if not validshopid.validshopid(shopid, driver):
                print str(shopid) + " not a validshopid, break"
                notvaliddata = open("../data/shopinfo_" + str(step) + ".txt", "w")
                notvaliddata.write(str(shopid) + ": not valid")
                notvaliddata.close()
                time.sleep(random.randint(3, 5))
                continue
            elif validshopid.validshopid(shopid, driver):
                time.sleep(random.randint(3, 5))
                print "collecting " + str(shopid) + "\'s infomation"
                data = open("../data/shopinfo_" + str(step) + ".txt", "w")
                shop = shopinfo_crawler.getshopinfo(str(shopid), driver)
                data.write(shop.getstr())
                time.sleep(random.randint(3, 5))

                print "collecting " + str(shopid) + "\'s m_info"
                mshop = mshop_crawler.getmshopinfo(str(shopid), driver)
                data.write(mshop.getstr())
                time.sleep(random.randint(3, 5))

                # if shop.data["istuan"] != 0:
                print "collecting " + str(shopid) + "\'s tuangou"
                data.write(alltuan_crawler.getalltuan(
                    str(shopid), driver, shop.data["istuan"]).getstr())
                time.sleep(random.randint(3, 5))

                print "collecting " + str(shopid) + "\'s reviewinfo"
                data.write(reviewinfo_crawler.getreviews(
                    str(shopid), driver, shop.data["review_total"]).getstr())
                time.sleep(random.randint(3, 5))

                print "collecting " + str(shopid) + "\'s messagewall"
                data.write(
                    msg_crawler.getmsginfo(str(shopid), driver, mshop.data["signnum"]).getstr())
                time.sleep(random.randint(3, 5))
                print "collecting " + str(shopid) + "\'s signinfo"
                data.write(
                    signinfo_crawler.getsigninfo(str(shopid), driver, mshop.data["signnum"]).getstr())
                time.sleep(random.randint(3, 5))
                data.close()
            print "data saved, continue"
            time.sleep(random.randint(3, 5))

        except Exception, ex:
            f = open("../log.txt", "a")
            traceback.print_exc(file=f)
            f.flush()
            f.close()
    driver.close()

time1 = time.ctime()
getshopinfo(int(sys.argv[1]))
time2 = time.ctime()
message = "Done! Running from %s to %s"
timemessage = (str(time1), str(time2))
print message % timemessage
