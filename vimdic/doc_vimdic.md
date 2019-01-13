# BeautifulSoup 사용법


# tag 찾기

```
for card in soup.find_all('div', {'class': 'card_word'}):
         subject = card.find('h4', {'class': 'tit_word'})
	 print subject
```	
이렇게 해도 되는데 걍 다음과 같이 해도됨!! soup.h4 객체가 아얘 생성되어있음.


```
for card in soup.find_all('div', {'class': 'card_word'}):
         print card.h4
```	



##

만약 다음과같이 subject 라는 soup 객체를 얻어왔다면

```python
for card in soup.find_all('div', {'class': 'card_word'}):
        subject = card.find('h4', {'class': 'tit_word'})
```
그  text를 출력하고 싶을때는 subject.text 보다는 다음과 같이 하면된다.


```
 print subject.contents[0]
```

## soup.prettify() 사용법

```
 print subject.prettify()
```

https://stackoverflow.com/questions/16835449/python-beautifulsoup-extract-text-between-element
