from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings
import time, pickle, os.path
import twint
import re


def write_log(text):
	f = open("Initialization/log.txt", "a+")
	f.write(text + "\n")
	f.close()


def get_time():
	
	f = open("Initialization/time.txt",'r')
	prev_since_time = f.read().replace(' ','').replace('\n','')
	f.close()

	run_time = datetime.strptime(prev_since_time, "%Y-%m-%d")
	until = run_time.strftime("%Y-%m-%d")
	run_time = run_time - timedelta(hours=24)
	since = run_time.strftime("%Y-%m-%d")

	return until, since


def save_time():
	until, since = get_time()
	f = open("Initialization/time.txt",'w')
	f.write(since)
	f.close()


def remove_html_tags(s):

	res = re.sub(r'<.*?>', '', s)
	res = re.sub("&amp;", "", res)
	res = re.sub("&nbsp", "", res)
	res = re.sub(";current positions", "", res)
	return res


def get_string(content, start, end):

	start_index = content.find(start)
	end_index = content.find(end, start_index)

	return content[start_index : end_index ]

def get_file_name(until):
	return "Data/" + str(until) + '.csv'