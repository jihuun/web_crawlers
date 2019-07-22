# This Python file uses the following encoding: utf-8
# Run with python 3 >
# Author: Ji-Hun Kim (jihuun.k@gmail.com)
# v

import time
import urllib
import urllib.request
import requests
from bs4 import BeautifulSoup


def make_url(input_word):
	return 'https://small.dic.daum.net/search.do?q=' + input_word + '&dic=eng&search_first=Y'

def get_urlreq(url, crt=None):
        f = requests.get(url, verify=crt)
        return f

if __name__  == "__main__":

        input_word = 'monopoly'

        url = make_url(input_word)
        page_src = get_urlreq(url, '/home/jihuun/Public/sa...ng.crt')
        soup = BeautifulSoup(page_src.text, "html.parser")

        # <ul class="list_search"> 아래있는 <li>..</li> 긁어옴
        test = soup.select('.list_search li') #
        for mean in test:
                print(mean.text)

        # test #2
        for card in soup.find_all('div', {'name': 'searchWords'}):
                print(card.text)
'''
        # test #3
        for card in soup.find_all('a', {'class': 'txt_searchword'}):
                try:
                        print(' ')
                        #print(card)
                        #print(card.text)

                except:
                        pass
'''

