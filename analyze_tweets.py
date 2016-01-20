#!/usr/bin/python3
""" This script analyzes tweets stored in a csv file and prints out statistics
    about them. """

import csv
import argparse
import datetime
import sys
import matplotlib.pyplot as plt
import tweepy
import json

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help=("read tweets from FILE "
                                          "(default: %(default)s)"),
                    default="tweets.csv")
parser.add_argument("-t", "--time", help=("analzye tweets from this time "
                                          "period (default: %(default)s)"),
                    default="day", choices=['hour', 'day', 'week'])
parser.add_argument("-g", "--hashtags", help=("keep stats on these hashtags "
                                              "(default: %(default)s)"),
                    default="#FalconPD,#MillLakeIsGreat,#GreatDayToBeAFalcon,#FabFalcons,#There'sNoPlaceLikeOakTree,#WeAreBrookside,#WLCares")
parser.add_argument("-p", "--pieoutput", help=("output pie chart to PIEOUTPUT "
                                               "(default: %(default)s)"),
                    default="/home/ryan/falconPD_website/assets/pie.svg")
parser.add_argument("-m", "--template", help=("location of markdown template "
                                              "default: %(default)s"),
                    default="templates/04-Daily Summary.md.template")
parser.add_argument("-o", "--mdoutput", help=("output markdown to MDOUTPUT "
                                              "(default: %(default)s)"),
                    default="/home/ryan/falconPD_website/_features/04-Daily Summary.md")
parser.add_argument("-a", "--access_tokens_file", help=("get access tokens "
						   "from this file. "
						   "(default: %(default)s)"),
		    default="access_tokens.json")

# Handle options stuff
args = parser.parse_args()
print("Getting access_tokens from:", args.access_tokens_file)
try:
    access_tokens_file = open(args.access_tokens_file, 'r')
    access_tokens = json.load(access_tokens_file)
    access_tokens_file.close()
except:
    print("Can't open access tokens file.")
    sys.exit(1)
print("Reading tweets from:", args.file)
start_datetime = datetime.datetime.utcnow()
print("All times are in UTC")
print("The current date and time is:", start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
if args.time == "hour":
    start_datetime -= datetime.timedelta(hours=1)
elif args.time == "day":
    start_datetime -= datetime.timedelta(days=1)
elif args.time == "week":
    start_datetime -= datetime.timedelta(weeks=1)
else:
    print("Invalid time specified")
    sys.exit(1)
print("Analyzing tweets starting with the following date and time:",
      start_datetime.strftime("%Y-%m-%d %H:%M:%S"))
hashtags = dict()
for hashtag in args.hashtags.split(','):
    hashtags[hashtag] = 0

# Create Stats
retweets = dict()
favorites = dict()
most_retweeted = "None"
most_favorited = "None"
try:
    csvfile = open(args.file, 'r', newline='')
    csv_input = csv.reader(csvfile, dialect='excel')
    next(csv_input) # skip the first row, it's a header
    total_tweets = 0
    for row in csv_input:
        this_datetime = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        if this_datetime > start_datetime:
            total_tweets += 1
            if (row[5] != ""):
                if row[5] in retweets:
                    retweets[row[5]] += 1
                else:
                    retweets[row[5]] = 1
            favorites[row[2]] = favorites.get(row[2], 0) + int(row[4])
            for hashtag in hashtags:
                if hashtag.lower() in row[3].lower():
                    hashtags[hashtag] += 1
    if (len(retweets) > 0):
        most_retweeted = max(retweets, key=retweets.get)
    if (len(favorites) > 0):
        most_favorited = max(favorites, key=favorites.get)
except FileNotFoundError:
    print(args.file, "not found.")
    sys.exit(1)
csvfile.close()

# Generate output

# Send out tweets to the most retweeted and most favorited
auth = tweepy.OAuthHandler(access_tokens['consumer_key'], access_tokens['consumer_secret'])
auth.set_access_token(access_tokens['access_token'], access_tokens['access_token_secret'])
api = tweepy.API(auth)
if (most_retweeted != "None"):
    api.update_status("Congrats @" + most_retweeted + " for being yesterday's most retweeted falcon! http://falconpd.github.io/#Daily%20Summary")
if (most_favorited != "None"):
    api.update_status("Congrats @" + most_favorited + " for being yesterday's most favorited falcon! http://falconpd.github.io/#Daily%20Summary")

# Make a pie chart showing the amount of tweets for each hashtag, pull out the
# hashtags that don't have any tweets
sizes = list()
labels = list()
for key, value in sorted(hashtags.items()):
    if value != 0:
        sizes.append(value)
        labels.append(key)
plt.pie(sizes, labels=labels, shadow=True, startangle=90, autopct='%1.0f%%')
plt.axis('equal')
plt.savefig(args.pieoutput, bbox_inches='tight')

# Read from the template, replace the tags with our variables
print("Total Tweets:", total_tweets)
print("Most Retweeted:", most_retweeted)
print("Most Favorited:", most_favorited)
f = open(args.template, 'r') 
filedata = f.read()
f.close()
filedata = filedata.replace("<TOTALTWEETS>", str(total_tweets))
filedata = filedata.replace("<MOSTRETWEETED>","@" + most_retweeted)
filedata = filedata.replace("<MOSTFAVORITED>","@" + most_favorited)
filedata = filedata.replace("<DATERUN>", datetime.datetime.today().strftime("%A %B %d, %Y"))
text_hashtags = ""
for hashtag in args.hashtags.split(','):
    text_hashtags += hashtag + ", "
text_hashtags =  text_hashtags[:-2] # Trim off the last ", "
filedata = filedata.replace("<HASHTAGS>", text_hashtags)
f = open(args.mdoutput,'w')
f.write(filedata)
f.close()
