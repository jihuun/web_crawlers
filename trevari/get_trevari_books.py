# This Python file uses the following encoding: utf-8
# Scraping all of the book list on trevari meetings
# Author: Ji-Hun Kim (jihuun.k@gmail.com)
# v 0.0.2

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
	#driver.implicitly_wait(10)	# Doesn't work at all
	drv.get(url)
	return drv

# For click the button "더 보기"
def click_next_btn(cnt, drv):
	while cnt > 0:
		# Copy xpath of the button from the chrome-dev mode
		#drv.find_element_by_xpath("""//*[@id="__next"]/div/div[2]/div/div/div[2]/button""").click()
		drv.find_element_by_xpath(g_button_xpath).click()
		time.sleep(1)	# It needs a time to wait a page fully loaded
		cnt = cnt - 1

if __name__  == "__main__":

	driver = get_webdriver(g_url)

	click_next_btn(10, driver)

	soup = BeautifulSoup(driver.page_source, "html.parser")

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

			if book_name != "읽을거리 정하는 중":
				print ("\"%s\" \t(%s, %s %s %s)" %(book_name, group_name, date_simple[1], date_simple[3], date_simple[4]))
				book_cnt = book_cnt + 1
		except:
			pass

		
	print ("총 %d 개" %(book_cnt))
