import os, re
import pandas as pd
from util import *
import requests
import json
from datetime import datetime, timedelta
import numpy as np
import warnings
import time, pickle, os.path
import twint
import requests


def get_links(content):
	links = []
	indices = [m.start() for m in re.finditer('class="btn btn-link', content)]

	for index in indices:
		link_buffer = get_string(content[index - 1 :], 'class="btn btn-link', '</a>')
		link_url = link_buffer[link_buffer.find('href="') : link_buffer.find('"', link_buffer.find('href="') + len('href="'))][len('href="'):]
		link_title = link_buffer[link_buffer.find('data-link-title="') : link_buffer.find('"', link_buffer.find('data-link-title="') + len('data-link-title="'))][len('data-link-title="'):]
		if len(link_url) > 1:
			links.append({'url': link_url, 'title': link_title })
	
	d = {}
	for i in range(len(links)):
		d[i] = links[i]

	return d, len(links)


def get_image(content):

	profile_photo = remove_html_tags (get_string(content, '<img class="user-img" src="', '" alt="Profile Image">')[len('<img class="user-img" src="'):])

	if profile_photo == 'https://d1qr63pinnvtia.cloudfront.net/assets/9d93dbd74c4342e6f8fa774ff2b18fb91799ab31/images/default_profile_picture.png':
			return ""
	else:
		return profile_photo

def get_username(content):

	username = remove_html_tags(get_string(content, '<a class="user-name btn">','</a>')).replace(" ","").replace("@","").replace('\n',"")
	return username

def get_link_tree_info(link_tree_link):
	try:

		headers = {'User-Agent' : 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
		result = requests.get(link_tree_link, headers = headers)
		content = result.text
		username = get_username(content)
		profile_photo = get_image(content)
		links, num_of_links = get_links(content)
		
		if num_of_links > 0 or profile_photo != "":
			return [username, profile_photo, links, num_of_links]
		else:
			return ["", "", "", ""]
	except Exception as e:
		print(e)
		return ["", "", "", ""]


if __name__ == '__main__':
	
	until, since = get_time()
	filename = get_file_name(until)
	Tweets_df = pd.read_csv(filename)
	Tweets_df[['LT_username', 'LT_profile_photo','LT_links','LT_number_of_links']] = Tweets_df.apply(lambda x: get_link_tree_info(x['linktree_link']), result_type = 'expand', axis = 1)
	Tweets_df = Tweets_df[Tweets_df['LT_username'] != ""]
	filename = get_file_name(until)
	Tweets_df.to_csv(filename)

	write_log("Got Information for " + str(Tweets_df.shape[0]) +   " users from " + until)
	save_time()
	os.system("python3 get_link_tree_tweets_from_twitter.py")