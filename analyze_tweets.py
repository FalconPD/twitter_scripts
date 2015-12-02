#!/usr/bin/python3
""" This script analyzes tweets stored in a csv file and prints out statistics
    about them. """

import csv
import argparse
import datetime
import sys
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help=("read tweets from FILE "
                                          "(default: %(default)s)"),
                    default="tweets.csv")
parser.add_argument("-t", "--time", help=("analzye tweets from this time "
                                          "period (default: %(default)s)"),
                    default="day", choices=['hour', 'day', 'week'])
parser.add_argument("-g", "--hashtags", help=("keep stats on these hashtags "
                                              "(default: %(default)s)"),
                    default="#FalconPD,#MillLakeIsGreat,#GreatDayToBeAFalcon,#FabulousFalcons")

# Handle options stuff
args = parser.parse_args()
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
            favorites[row[2]] = favorites.get(row[2], 0) + int(row[4])
            retweets[row[2]] = retweets.get(row[2], 0) + int(row[5])
            for hashtag in hashtags:
                if hashtag.lower() in row[3].lower():
                    hashtags[hashtag] += 1
    count = 0
    for name in retweets:
        if retweets[name] > count:
            count = retweets[name]
            most_retweeted = name
    count = 0
    for name in favorites:
        if favorites[name] > count:
            count = favorites[name]
            most_favorited = name
except FileNotFoundError:
    print(args.file, "not found.")
    sys.exit(1)
csvfile.close()

# Generate output

# Make a pie chart showing the amount of tweets for each hashtag, pull out the
# hashtags that don't have any tweets
sizes = list()
labels = list()
for hashtag in hashtags:
    if hashtags[hashtag] != 0:
        sizes.append(hashtags[hashtag])
        labels.append(hashtag)
plt.pie(sizes, labels=labels, shadow=True, startangle=90)
plt.axis('equal')
plt.savefig("test.png")
print("Total Tweets:", total_tweets)
print("Most Retweeted:", most_retweeted)
print("Most Favorited:", most_favorited)
