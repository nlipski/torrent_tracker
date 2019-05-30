import urllib.request
from bs4 import BeautifulSoup


def parse_season_n_episode(word):
	if len(word) == 6 and word[1].isdigit():

		season = int (word[1] + word[2])
		episode = int (word[4] + word[5])
		return season, episode
	elif len(word) == 3 and word[1].isdigit():
		season = int (word[1] + word[2])
		return season, -1
	else:
		return -1, -1

def parse_name(name,num_of_words):

	sep = '.'
	name = name.strip()
	under = name.find('_')
	dot = name.find('.')
	space = name.find(' ')
	print(name)

	if (under > 0) and ((dot == -1) or (under <= dot)) and ((space == -1) or(under <= space)):
		sep = '_'
	elif (dot > 0) and ((under == -1) or (under >= dot)) and ((space == -1) or (dot <= space)):
		sep = '.'
	elif (space > 0) and ((dot == -1) or (space <= dot)) and ((under == -1) or (under >= space)) :
		sep = ' '
	else:
		return None

	info_list = name.split(sep)

	series_name = ""
	for i in range(num_of_words):
		series_name = series_name + ' ' + info_list[i]
	
	series_name = series_name.strip()
	season = -1
	episode = -1
	quality = -1
	if len(info_list[num_of_words]) % 3 == 0:
		season, episode = parse_season_n_episode(info_list[num_of_words])

	#if info_list[]
	print(series_name)
	print(season)
	print(episode)

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
headers['Accept'] = "text/html"
headers['Accept-Charset'] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
headers['Accept-Encoding'] = "none"
headers['Accept-Language'] = "en-US,en;q=0.8"
headers['Connection'] = "keep-alive"

space = '%20'
series_name = " family guy  "
series_name = (series_name.strip()).replace(' ', space)
num_of_words = series_name.count(space) + 1
print(num_of_words)
full_url = "https://thepiratebay.org/s/?q="+series_name+"&video=on&category=0&page=0&orderby=99"

request = urllib.request.Request(full_url, headers= headers)

htmlfile = urllib.request.urlopen(request)
htmltext = htmlfile.read()

soup = BeautifulSoup(htmltext, 'html.parser')

i = 0
for row in soup.find_all('tr'):
	name = row.find('a', class_='detLink')
	magnet = row.find('a', title = "Download this torrent using magnet")
	
	if name == None or magnet == None:
		continue

	name = name.text
	magnet = magnet.get('href')
	title_info = parse_name(name, num_of_words)

	#print(i)	
	#print(name.text)
	#print(magnet.get('href'))

	i += 1
	
	print("\n\n\n")
#print (soup.prettify())
