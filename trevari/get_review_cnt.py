#-*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
# Scraping all of the book list on trevari meetings
# Run with python 2.7
# Author: Ji-Hun Kim (jihuun.k@gmail.com)
# v 0.1.1

import time
import urllib
import requests
from os.path import expanduser
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

g_url='https://trevari.co.kr'

g_url_clubpage='https://trevari.co.kr/meetings/show?clubID=e1431305-6f5e-4283-b79a-a65311b1d896&order=1'
g_url_login='https://trevari.co.kr/login'
g_url_meetings='https://trevari.co.kr/meetings'

g_output_file='trevari_review_count'
g_output_file='test_list_with_review_count'
g_login_file=expanduser('~') + '/.web_crawlers_login/trevari/.login'
g_id=None
g_pw=None

g_button_xpath="""//*[@id="__next"]/div/div[2]/div/div/div[2]/button"""
id_xpath='//*[@id="__next"]/div/div[2]/div[1]/div/div/form/input[1]'
pw_xpath='//*[@id="__next"]/div/div[2]/div[1]/div/div/form/input[2]'
login_button_xpath='//*[@id="__next"]/div/div[2]/div[1]/div/div/form/button'

def get_url(drv, url):
	drv.get(url)
	time.sleep(2)
	return drv

def get_g_id_pw():
        f = open(g_login_file, 'r')
        line = f.readlines()
        f.close()
        return line[0][:-1], line[1][:-1]

def auto_login(drv):
        if g_id and g_pw:
                drv = get_url(drv, g_url_login)
                drv.find_element_by_xpath(id_xpath).send_keys(g_id) #FIXME: needs cryption
                drv.find_element_by_xpath(pw_xpath).send_keys(g_pw)
                drv.find_element_by_xpath(login_button_xpath).click()
                # TODO: Do not wait with a static time
                time.sleep(5) # TODO: needs wait ? yes
        else:
                print 'Can not login because of no ID/PW'

def get_clubpage_src(drv):
        drv = get_url(drv, g_url_clubpage)
        return drv

def get_webdriver():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('disable-gpu')

	drv = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
	#drv.implicitly_wait(10)	# Doesn't work at all
	time.sleep(2)
        return drv


def get_review_count(url):
	driver_club = get_webdriver()
        auto_login(driver_club)
        driver_club = get_url(driver_club, url)

	soup = BeautifulSoup(driver_club.page_source, "html.parser")
	time.sleep(2)
#        print soup

        member_cnt = 0
        travler_cnt = 0

        #for review in soup.find_all('div', {'style':'padding:20px'}):
        for review in soup.find_all('div', {'class':'jsx-4121886606 bookreview-item'}):
		try:
                        #print '--------------'
                        #print review
                        member_classify_tag = review.find('div', {'style':'color:#ff8906;margin-bottom:3px'})
                        if member_classify_tag:
                                who = member_classify_tag.get_text() # get_text return unicode
                                #print who.encode('utf-8') # get_text().encode('utf-8') make 'str'

                                if who == u"놀러가기":
                                        travler_cnt = travler_cnt + 1
                                elif who == u"멤버" or who == u"파트너":
                                        member_cnt = member_cnt + 1

                except Exception as ex: # 에러 종류
                        print('Exception occured', ex) # ex는 발생한 에러의 이름을 받아오는 변수
                        pass

	#driver_club.close()
	driver_club.quit()

        return travler_cnt, member_cnt

if __name__  == "__main__":
        #url = g_url_clubpage
        #url = 'https://trevari.co.kr/meetings/show?clubID=59aac5cc-a12a-486c-9c27-3b13cd624c65&order=1'
        #url = 'https://trevari.co.kr/meetings/show?clubID=95652008-0a45-41c4-9ee6-182693d1a957&order=1'
        #url = 'https://trevari.co.kr/meetings/show?clubID=0838373c-699d-4a25-ba49-6c87522a3e5a&order=1'
        #url = 'https://trevari.co.kr/meetings/show?clubID=8cce5a39-3da1-4933-8b9f-786189bcd761&order=1'

        g_id, g_pw = get_g_id_pw()

        url = 'https://trevari.co.kr/meetings/show?clubID=ad437199-caf5-4243-b82e-95ba66a3f423&order=1'

        travler_cnt, member_cnt = get_review_count(url);
        print '놀러가기/멤버 %d / %d' %(travler_cnt, member_cnt)

'''
        url = 'https://trevari.co.kr/meetings/show?clubID=8995cf36-e673-4cff-8cb7-cb35b7966890&order=1'
        travler_cnt, member_cnt = get_review_count(url);
        print '놀러가기/멤버 %d / %d' %(travler_cnt, member_cnt)
'''
