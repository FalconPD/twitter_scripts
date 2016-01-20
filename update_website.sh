#!/bin/bash

PATH=$PATH:/usr/local/bin
HASHTAGS="#FalconPD,#MillLakeIsGreat,#GreatDayToBeAFalcon,#FabFalcons,#There'sNoPlaceLikeOakTree,#WeAreBrookside,#WLCares"

cd /home/ryan/twitter_scripts
./get_tweets.py -g ${HASHTAGS}
./analyze_tweets.py -g ${HASHTAGS}
cd ../falconPD_website
jekyll build
git add "_features/04-Daily Summary.md" assets/pie.svg
git commit -m "automatic daily update"
git push
cd ../FalconPD.github.io
git add *
git commit -m "automatic daily update"
git push
