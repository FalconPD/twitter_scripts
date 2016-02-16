#!/usr/bin/python3
""" This script downloads tweets that match a certain search expression to a
    csv file """

#FIXME This unicode stripping is awful
def stripUnicode(str):
    return str.encode('ascii', 'ignore').decode('ascii')

import tweepy
import csv
import json
import sys
import argparse

# Handle options stuff
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help=("append tweets to FILE. If it does "
					  "not exist it will be created. "
					  "(default: %(default)s)"),
		    default="tweets.csv")
parser.add_argument("-g", "--hashtags", help=("collect tweets with these "
					      "hashtags (default: "
					      "%(default)s)"),
		    default="#FalconPD,#MillLakeIsGreat,#GreatDayToBeAFalcon,#FabFalcons,#TheresNoPlaceLikeOakTree,#WeAreBrookside,#WLCares,#BBRocks,#ApplegarthFalcons")
parser.add_argument("-a", "--access_tokens_file", help=("get access tokens "
						   "from this file. "
						   "(default: %(default)s)"),
		    default="access_tokens.json")
parser.add_argument("-b", "--blacklist_file", help=("ignore tweets from"
                                                    " these handles. "
                                                    "(default: %(default)s)"),
                    default="blacklist.json")

args = parser.parse_args()
print("Writing tweets to:", args.file)
print("Getting access_tokens from:", args.access_tokens_file)
print("Using blacklist file:", args.blacklist_file)
search_string=str()
for hashtag in args.hashtags.split(','):
	search_string += hashtag + " OR "
search_string = search_string[:-4] #Trim off the last " OR "
print("Using search string:", search_string)

try:
    access_tokens_file = open(args.access_tokens_file, 'r')
    access_tokens = json.load(access_tokens_file)
    access_tokens_file.close()
except:
    print("Can't open access tokens file.")
    sys.exit(1)

try:
    blacklist_file = open(args.blacklist_file, 'r')
    blacklist = json.load(blacklist_file)
    blacklist_file.close()
except:
    print("Can't open blacklist file.")
    sys.exit(1)

print("Ignoring tweets from:", ", ".join(blacklist))

auth = tweepy.OAuthHandler(access_tokens['consumer_key'], access_tokens['consumer_secret'])
auth.set_access_token(access_tokens['access_token'], access_tokens['access_token_secret'])
api = tweepy.API(auth)

# Get the last tweet ID that we stored
last_id = 0
try:
    csvfile = open(args.file, 'r', newline='')
    csv_input = csv.reader(csvfile, dialect='excel')
    for row in csv_input: # FIXME: There has to be a better way to get to the last row
        last_id = row[0]
except FileNotFoundError:
    print(args.file, "not found, it will be created.")
    csvfile = open(args.file, 'a', newline='')
    csv_output = csv.writer(csvfile, dialect='excel')
    csv_output.writerow(["id", "created_at (UTC)", "screen_name", "text",
                         "favorite_count", "original screen_name"])
csvfile.close()

print("Getting all tweets since id", last_id)

# Get all the tweets from the last one we stored
tweets = list()
for tweet in tweepy.Cursor(api.search, search_string, since_id=last_id).items():
    tweets.append(tweet)
tweets.reverse() # Make oldest tweet first and the newest tweet last
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
csvfile.close()
