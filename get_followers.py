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

for user in tweepy.Cursor(api.friends).items():
        print(user.screen_name)
        time.sleep(1)
for user in tweepy.Cursor(api.followers).items():
        print(user.screen_name)
        time.sleep(1)
