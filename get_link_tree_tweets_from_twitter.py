from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import time, os.path
import twint
import re
from util import *
import os


def get_linktree_link(tweet):
    
    tweets = tweet.split(" ")
    for word in tweets:
        if word[ : len('https://linktr.ee/')] == 'https://linktr.ee/':
            return word
    return ""


if __name__ == '__main__':
	
	until, since = get_time()

	client = twint.Config()
	client.Search = 'linktr.ee'
	client.Pandas = True
	client.Since = since
	client.Until = until
	client.Hide_output = True
	
	objects = twint.run.Search(client)
	Tweets_df = twint.storage.panda.Tweets_df

	Tweets_df = Tweets_df.drop(['cashtags','search','translate', 'trans_src', 'trans_dest'], axis = 1)
	Tweets_df['linktree_link'] = Tweets_df.apply(lambda x: get_linktree_link(x['tweet']), result_type = 'expand', axis = 1)
	Tweets_df = Tweets_df[Tweets_df['linktree_link'] != ""]
	Tweets_df = Tweets_df.drop_duplicates(subset = 'linktree_link')

	filename = get_file_name(until)
	Tweets_df.to_csv(filename)

	write_log("saving " + str(Tweets_df.shape[0]) +   " tweets from " + until)
	os.system("python3 get_link_tree_info_from_tweets.py")