#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 21:35:59 2021

@author: emilywang
"""
# ============================================================================
# Spotify Project 

import pandas
from matplotlib import pyplot as plt
import numpy
import seaborn

# endTime: day/time th song was finished, in UTC format
# artistName: name of artist
# trackName: name of song
# msPlayed: how long (i milliseconds) the song was played

streaming = pandas.read_json('StreamingHistory0.json')
streaming.head(5)
streaming.to_csv('SpotifyStream.csv') # save as csv data

# Information of the dataframe
streaming.shape # (7508 rows x 4 columns)
streaming.info() # information
streaming.nunique() # unique elements present in each column (846 unique artists out of 7508)
streaming.sample(10) # prints out a random sample of 10

len(streaming['artistName'].unique()) # 846 unique artists
len(streaming['trackName'].unique()) # 2514 unique tracks



# Cleaning and formatting ====================================================
streaming['playTime'] = pandas.to_datetime(streaming['endTime']) # converting object column to proper date-time column
streaming['year'] = pandas.DatetimeIndex(streaming['playTime']).year # year song played
streaming['month'] = pandas.DatetimeIndex(streaming['playTime']).month # month song played 
streaming['day'] = pandas.DatetimeIndex(streaming['playTime']).day # day song played 
streaming['weekday'] = pandas.DatetimeIndex(streaming['playTime']).weekday # weekday song played 
streaming['time'] = pandas.DatetimeIndex(streaming['playTime']).time # time song played 
streaming['hour'] = pandas.DatetimeIndex(streaming['playTime']).hour # hour song played
streaming['dayName'] = streaming['playTime'].apply(lambda x: x.day_name()) # dayName of song played
streaming['count'] = 1 # to keep track of song count

streaming['timePlayed (hh-mm-ss)'] = pandas.to_timedelta(streaming['msPlayed'], unit = 'ms') # timeframe of song played in milliseconds (hour-min-sec)

# to get hour information
def hours(td):
    return td.seconds/3600
# to get minute information
def minutes(td):
    return(td.seconds/60)%60

streaming['Listening Time (hours)'] = streaming['timePlayed (hh-mm-ss)'].apply(hours).round(3) # convert time from 'TimePlayed' to approx. hours
streaming['Listening Time (minutes)'] = streaming['timePlayed (hh-mm-ss)'].apply(minutes).round(3) # convert time from 'TimePlayed' to approx. mins

streaming.drop(columns = ['endTime', 'timePlayed (hh-mm-ss)', 'msPlayed'], inplace = True) # removing columns from dataFrame
# inplace = True allows us to update dataframe rather than reassign it




# Data analysis ==============================================================
#uniqueArtists = streaming['artistName'].nunique() # 846 unique artists
#totalArtists = streaming['artistName'].count() # 7508 total artists
#uniqueArtistsPercent = uniqueArtists/totalArtists * 100 # we multiply 100 to get a percentage instead of decimal --> 11.27% unique artists


# Top 10 unique artists (by hr/min)
top10Artists = streaming.groupby(['artistName'])[['Listening Time (hours)', 'Listening Time (minutes)', 'count']].sum().sort_values(by = 'Listening Time (minutes)', ascending = False)
# we groupyby 'artistName' and then include the following columns for new dataFrame
top10Artists = top10Artists.head(10) # shows the top 10
# print(top10Artists.head(10))


# Top 10 unique artists (by listening count)
top10ArtistsCount = streaming.groupby(['artistName'])[['Listening Time (hours)', 'Listening Time (minutes)', 'count']].sum().sort_values(by = 'count', ascending = False)
top10ArtistsCount = top10ArtistsCount.head(10) # shows 10 most counted artists


# Top 10 unique songs (by min)
top10Songs = streaming.groupby(['trackName'])[['Listening Time (hours)', 'Listening Time (minutes)', 'count']].sum().sort_values(by = 'Listening Time (minutes)', ascending = False)
top10Songs = top10Songs.head(10)


# Top 10 unique songs (by listening count)
top10SongsCount = streaming.groupby(['trackName'])[['Listening Time (hours)', 'Listening Time (minutes)', 'count']].sum().sort_values(by = 'count', ascending = False)
top10SongsCount = top10SongsCount.head(10) # shows 10 most counted songs



# Data visualization =========================================================
# What are my top 10 artists from 12/3/20 to 12/4/21 (by hours)?
seaborn.barplot(x = top10Artists.index, y = top10Artists['Listening Time (hours)'], palette = 'icefire').set(
    xlabel = 'Artist & Podcast Name',
    ylabel = 'Hours Listened',
    title = 'Top 10 Artists & Podcasts (by hours)') 
pyplot.xticks(rotation = 90)


# histogram of songs played by hours
seaborn.histplot(x = 'hour', data = streaming, bins = 24, kde = True, color = 'darkcyan').set(
    xlabel = 'Hours (in 24 hours)',
    ylabel = 'Number of Streams',
    title = 'Average Usage Over 24 Hours')
pyplot.tight_layout()


# bargraph subplots of top 10 COUNTED songs/artists
fig, axes = plt.subplots(1,2, figsize = (20,5))
pyplot.tight_layout()
# Plot 1
seaborn.barplot(ax = axes[0], x = top10ArtistsCount.index, y = top10ArtistsCount['count'], color = 'rosybrown')
axes[0].set(title = 'Top 10 Artists & Podcasts (by count)',
            xlabel = 'Artists & Podcasts',
            ylabel = 'Number of Streams')
axes[0].tick_params(labelrotation = 87)
# Plot 2
seaborn.barplot(ax = axes[1], x = top10SongsCount.index, y = top10SongsCount['count'], color = 'cadetblue')
axes[1].set(title = 'Top 10 Songs (by count)',
            xlabel = 'Songs',
            ylabel = 'Number of Streams')
axes[1].tick_params(labelrotation = 87)



seaborn.barplot(y = top10ArtistsCount.index, x = top10ArtistsCount['count'], color = 'rosybrown').set(
    title = 'Top 10 Artists & Podcasts (by count)',
    ylabel = 'Artists & Podcasts',
    xlabel = 'Number of Streams')

seaborn.barplot(y = top10SongsCount.index, x = top10SongsCount['count'], color = 'cadetblue').set(
    title = 'Top 10 Songs (by count)',
    ylabel = 'Songs',
    xlabel = 'Number of Streams')

