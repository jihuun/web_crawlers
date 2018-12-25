# This Python file uses the following encoding: utf-8
# Scraping all of the book list on trevari meetings
# Run with python 2.7
# Author: Ji-Hun Kim (jihuun.k@gmail.com)
# v 0.0.5

import time
import urllib
import requests
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

g_url='https://trevari.co.kr/meetings'
g_button_xpath="""//*[@id="__next"]/div/div[2]/div/div/div[2]/button"""

def get_webdriver(url):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('disable-gpu')

	drv = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
	#drv.implicitly_wait(10)	# Doesn't work at all
	time.sleep(2)
	drv.get(url)
	time.sleep(2)
	return drv

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

def print_subject():
	print("<트레바리 클럽 별 선정 도서 목록>")
	print("Updated on %s" %(print_current_time()))

if __name__  == "__main__":

	driver = get_webdriver(g_url)
	scroll_down(40, driver)
	soup = BeautifulSoup(driver.page_source, "html.parser")

	print_subject()

	book_cnt = 0
	for meeting in soup.find_all('a'):
		try:
			book = meeting.find('div', {'style':'font-weight: 600;'})
			book_name = book.get_text()
			
			group = meeting.find('div', {'style':'font-weight: bold;'})
			group_name = group.get_text()

			date = meeting.find('div', {'style':"color: rgb(123, 123, 123); font-size: 14px; margin-top: 4px;"})
			date_text = date.get_text()
			date_simple = date_text.split(' ')

			if book_name != u"읽을거리 정하는 중":
				print ("\"%s\" \t(%s, %s %s %s)" %(book_name, group_name, date_simple[0], date_simple[2], date_simple[3]))
				book_cnt = book_cnt + 1
		except:
			pass

		
	print ("총 %d 개" %(book_cnt))
