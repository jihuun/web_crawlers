# This Python file uses the following encoding: utf-8
# 
# Author: Ji-Hun Kim (jihuun.k@gmail.com)
# v 0.0.1
# using python2.7

import time
import urllib
import requests
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

g_url='https://translate.google.com/#en/ko/'

#https://translate.google.co.kr/#en/ko/Type%20text%20or%20a%20website%20address%20or%20translate%20a%20document.

def gen_url(source):
	url = g_url
	return url + urllib.quote(source)


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

if __name__  == "__main__":

	driver = get_webdriver(g_url)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	url = gen_url('Type text or a website address or translate a document.')

	result = soup.find("span",{"id": "result_box"})
# driver.page_source자체에 한글번역된 문장 자체가 없다.. 크롤링 불가..? 180729

	#result = soup.find(id="gt-res-dir-ctr")
	#result = soup.find(id="gt-res-c")
	#result = soup.find('div', {'class':'g-unit'})
	print ("%s" %result)
###
# <span id="result_box" class="" lang="ko"><span class="">텍스트 또는 웹 사이트 주소를 입력하거나 문서를 번역하십시오.</span></span>
		
# <div id="gt-res-dir-ctr" dir="ltr" class="trans-verified-button-small"><span id="gt-res-error" style="display:none"></span><span id="result_box" class="" lang="ko"><span class="">텍스트 또는 웹 사이트 주소를 입력하거나 문서를 번역하십시오.</span></span><span id="t-served-community-button" class="trans-verified-button goog-toolbar-button" role="button" aria-hidden="true" style="display: none; user-select: none;"><span class="jfk-button-img"></span></span></div>

#table_div = soup.find(id="sdetail")
#tables = table_div.find_all("table")
#menu_table = tables[1]
#trs = menu_table.find_all('tr')
