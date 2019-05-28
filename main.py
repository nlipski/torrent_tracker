import urllib.request
from bs4 import BeautifulSoup



headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
headers['Accept-Charset'] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
headers['Accept-Encoding'] = "none"
headers['Accept-Language'] = "en-US,en;q=0.8"
headers['Connection'] = "keep-alive"

full_url = "https://thepiratebay.org/s/?q=chernobyl&video=on&category=0&page=0&orderby=99"

request = urllib.request.Request(full_url, headers= headers)
htmlfile = urllib.request.urlopen(request)

htmltext=htmlfile.read()
soup = BeautifulSoup(htmltext, 'html.parser')
for row in soup.find_all('tr'):
	for column in row.find_all('td'):
		print(type(column))
	print("\n\n\n")
#print (soup.prettify())
