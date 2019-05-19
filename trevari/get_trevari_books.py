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

NR_SCROLL_DN=1

g_url='https://trevari.co.kr'
g_url_login='https://trevari.co.kr/login'
g_url_meetings='https://trevari.co.kr/meetings'

g_output_file='trevari_book_list'
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

# NOTE: Auto login feature
# You should make a file that has ID/PW of trevari on ~/.web_crawlers_login/trevari/.login
# Simply put your ID and PW on the file over 2 line
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


def get_webdriver():
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('disable-gpu')

	drv = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
	#drv.implicitly_wait(10)	# Doesn't work at all
	time.sleep(2)
	return drv

# Get number of reviews on each club page
def get_review_count(url):
	driver_club = get_webdriver()
        auto_login(driver_club)
        driver_club = get_url(driver_club, url)
	soup = BeautifulSoup(driver_club.page_source, "html.parser")

        member_cnt = 0
        travler_cnt = 0

        for review in soup.find_all('div', {'class':'jsx-4121886606 bookreview-item'}):
		try:
                        member_classify_tag = review.find('div', {'style':'color:#ff8906;margin-bottom:3px'})
                        if member_classify_tag:
                                who = member_classify_tag.get_text() # get_text return unicode
                                #print who.encode('utf-8') # get_text().encode('utf-8') make 'str'
                                if who == u"놀러가기":
                                        travler_cnt = travler_cnt + 1
                                elif who == u"멤버" or who == u"파트너":
                                        member_cnt = member_cnt + 1

                except Exception as ex:
                        print('Exception occured from get_review_count', ex)
                        pass

	driver_club.quit()

        return travler_cnt, member_cnt

# For click the button "더 보기"
def click_next_btn(cnt, drv):
	while cnt > 0:
		# Copy xpath of the button from the chrome-dev mode
		drv.find_element_by_xpath(g_button_xpath).click()
		time.sleep(2)	# It needs a time to wait a page fully loaded
		cnt = cnt - 1

# For scrolling down to the end "cnt" times
def scroll_down(cnt, drv):
	while cnt > 0:
		drv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		cnt = cnt - 1

def print_current_time():
	now = time.localtime()
	s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
	return s

def print_subject(f):
	f.write("## 트레바리 클럽별 선정 도서 목록  \n")
	f.write("> Updated on %s  \n\n" %(print_current_time()))
	f.write("> This page has been generated automatically by %s which is open source project.  \n" %(md_make_hyperlink("a python script", "https://github.com/jihuun/web_crawlers/blob/master/trevari/get_trevari_books.py")))
	f.write("> Sharing this page, reporting bugs & new ideas, %s are always welcome :)  \n" %(md_make_hyperlink("pull requests", "https://github.com/jihuun/web_crawlers")))
	f.write("> Maintained by %s  \n\n" %(md_make_hyperlink("@soopsaram", "jihuun.k@gmail.com")))
	f.write("---\n\n")
	f.write("| 선정 도서 | 클럽 | 아지트 | 날짜 | 독후감(놀/멤) | \n")
	f.write("| --- | --- | --- | --- | --- | \n")

def md_make_hyperlink(src, link):
	return '[' + src + '](' + link + ')'

def get_href(meeting):
	href = meeting['href']
	return g_url + href

def split_place_date(word_list):
        str_by_list = ' '.join(word_list)
        split_str = str_by_list.split(u'2019년')
	place = split_str[0].split()
	place_result = '%s' %place[0]
	date = split_str[1].split()
	date_result = '%s %s' %(date[0], date[1])

        return place_result, date_result

if __name__  == "__main__":

        driver = get_webdriver()
        driver = get_url(driver, g_url_meetings)
        scroll_down(NR_SCROLL_DN, driver)
	soup = BeautifulSoup(driver.page_source, "html.parser")
        g_id, g_pw = get_g_id_pw()

	f = open(g_output_file+'.md', 'w')
	print_subject(f)

	book_cnt = 0
        member_cnt = 0
        travler_cnt = 0
	for meeting in soup.find_all('a', href=True):
		try:
			book = meeting.find('div', {'style':'font-weight: 600;'})
			if book != None:
				book_name = book.get_text()

			if book_name != u"읽을거리 정하는 중":
                                group = meeting.find('div', {'style':'font-weight: bold;'})
                                if group != None:
                                        group_name = group.get_text()
                                        group_name_url = get_href(meeting)
                                        group_name_link = md_make_hyperlink(group_name, group_name_url)
                                        travler_cnt, member_cnt = get_review_count(group_name_url)

                                place_date = meeting.find('div', {'style':"color: rgb(123, 123, 123); font-size: 14px; margin-top: 4px;"})
                                if place_date != None:
                                        date_text = place_date.get_text()
                                        date_simple = date_text.split(' ')
                                        place, date = split_place_date(date_simple)

                                infos = ("| %s | %s | %s | %s | %d / %d | \n" %(book_name, group_name_link, place, date, travler_cnt, member_cnt))
                                f.write(infos.encode('utf-8'))
                                book_cnt = book_cnt + 1

                except Exception as ex:
                        print('Exception occured', ex)
			pass

	f.write("\n총 %d 개  \n\n" %(book_cnt))
	f.close()
	driver.quit()
