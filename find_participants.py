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
parser.add_argument("-f", "--file", help=("read tweets from FILE "
                                            "(default: %(default)s)"),
                    default="tweets.csv")
parser.add_argument("-a", "--access_tokens_file", help=("get access tokens "
						   "from this file. "
						   "(default: %(default)s)"),
		    default="access_tokens.json")

args = parser.parse_args()

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

# By using a set we will only keep the unique names
handles = set()

# Add everyone we follow
for user in tweepy.Cursor(api.friends).items():
    handles.add(user.screen_name)
    time.sleep(1)

# Add everyone who follows us
for user in tweepy.Cursor(api.followers).items():
    handles.add(user.screen_name)
    time.sleep(1)

# Add everyone who has used one of our hashtags
csvfile = open(args.file, 'r', newline='')
csv_input = csv.reader(csvfile, dialect='excel')
next(csv_input) # skip the first row, it's a header
for row in csv_input:
    handles.add(row[2])
csvfile.close()

for handle in handles:
    print(handle)
