import urllib.request
from bs4 import BeautifulSoup
from qbittorrent import Client

def init_header():

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
	headers['Accept'] = "text/html"
	headers['Accept-Charset'] = "ISO-8859-1,utf-8;q=0.7,*;q=0.3"
	headers['Accept-Encoding'] = "none"
	headers['Accept-Language'] = "en-US,en;q=0.8"
	headers['Connection'] = "keep-alive"
	return headers

class Title:
	def __init__(self, series_name, season, episode, quality, link):
		self.name = series_name
		self.season = season
		self.episode = episode
		self.quality = quality
		self.link = link



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

	return series_name, season, episode, quality

def create_title_list(htmltext, num_of_words):
	soup = BeautifulSoup(htmltext, 'html.parser')

	titles_list = []

	for row in soup.find_all('tr'):
		name = row.find('a', class_='detLink')
		magnet = row.find('a', title = "Download this torrent using magnet")
	
		if name == None or magnet == None:
			continue

		name = name.text
		magnet = magnet.get('href')
	
		series_name, season, episode, quality = parse_name(name, num_of_words)
		titles_list.append(Title(series_name, season, episode, quality, magnet))

	return titles_list

def prepare_name(series_name):
	space = '%20'
	series_name = (series_name.strip()).replace(' ', space)
	num_of_words = series_name.count(space) + 1
	
	return series_name, num_of_words

def create_search_link(series_name, headers, pagenum):
	

	full_url = "https://thepiratebay.org/s/?q="+series_name+"&video=on&category=0&page="+str(pagenum)+"&orderby=99"

	request = urllib.request.Request(full_url, headers= headers)

	htmlfile = urllib.request.urlopen(request)
	htmltext = htmlfile.read()

	return htmltext

def remove_unclassified(titles_list):

	return list(filter(lambda title: title.season != -1 or title.episode != -1 , titles_list))

# NEED TO DEAL WITH INCONSISTENCY WITH NAMES

def sort_by_season_episode(titles_list):

	return sorted(titles_list, key=lambda title: title.season, reverse = True)


headers = init_header()
series_name = "family guy   "
series_name, num_of_words = prepare_name(series_name)
htmltext = create_search_link(series_name, headers, 0)
titles_list = create_title_list(htmltext, num_of_words)
titles_list = remove_unclassified(titles_list)
titles_list = sort_by_season_episode(titles_list)
for title in titles_list:
	print(title.season)