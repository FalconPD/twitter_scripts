#!/usr/bin/python3
""" This script download FalconPD's followers to a csv file """

import tweepy
import csv
import json
import sys
import argparse
import time

# Handle options stuff
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--access_tokens_file", help=("get access tokens "
						   "from this file. "
						   "(default: %(default)s)"),
		    default="access_tokens.json")

args = parser.parse_args()
print("Getting access_tokens from:", args.access_tokens_file)

try:
    access_tokens_file = open(args.access_tokens_file, 'r')
    access_tokens = json.load(access_tokens_file)
    access_tokens_file.close()
except:
    print("Can't open access tokens file.")
    sys.exit(1)

auth = tweepy.OAuthHandler(access_tokens['consumer_key'], access_tokens['consumer_secret'])
auth.set_access_token(access_tokens['access_token'], access_tokens['access_token_secret'])
api = tweepy.API(auth)

for user in tweepy.Cursor(api.followers).items():
        print(user.screen_name)

"""
csvfile = open(args.file, 'a', newline='')
csv_output = csv.writer(csvfile, dialect='excel')
for tweet in tweets:
    if (tweet.user.screen_name in blacklist):
        print("Ignoring tweet from", tweet.user.screen_name)
    else:
        if hasattr(tweet, 'retweeted_status'):
            original_screen_name = stripUnicode(tweet.retweeted_status.user.screen_name)
        else:
            original_screen_name = ""
        screen_name = stripUnicode(tweet.user.screen_name)
        text = stripUnicode(tweet.text)
        print(tweet.id, tweet.created_at, screen_name, text, tweet.favorite_count, original_screen_name) 
        csv_output.writerow([tweet.id, tweet.created_at, screen_name, text, tweet.favorite_count, original_screen_name])
csvfile.close() """
