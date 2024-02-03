# -*- coding: utf-8 -*-
"""analysis-spotify.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mMaVVH-aKAFwkE9ZBnndXBsor0_UCSIR

## **Most Streamed Spotify Songs 2023**

### **Importing Libraries and Dataset**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import seaborn.objects as so

from google.colab import files

uploaded = files.upload()

df = pd.read_csv("spotify-2023.csv", encoding='latin-1')

"""### **Data Preparation and Data Cleaning**"""

df.head(10)

df.info()

print(df.isnull().sum())

"""#### **Checking of Values in the Dataset**

####  Null values

####  Incorrect datatypes

####  Pitch Class Notation

####  Additional Column
"""

## Replace null values in 'in_shazam_charts' column into 0
df['in_shazam_charts'].fillna(0, inplace=True)

## Replace invalid data in the 'stream' column into null
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

## Replace null values in 'key' column into 'none'
df['key'] = df['key'].fillna(-1)

## Drop the null value in the 'streams' column
df = df.dropna(how='any')

print(df.isnull().sum())

## Remove the comma (,) for some values in columns 'in_deezer_playlists' and 'in_shazam_charts' and convert them into int64
df['in_deezer_playlists'] = df['in_deezer_playlists'].replace(',', '', regex=True).astype('int64')
df['in_shazam_charts'] = df['in_shazam_charts'].replace(',', '', regex=True).astype('int64')

## Change the datatype of 'streams' column into int64
df['streams'] = df['streams'].astype('int64')

## Change values in 'key' column into integers using Pitch Class Notation
pitch_class = {'C': 0,
               'C#': 1,
               'D': 2,
               'D#': 3,
               'E': 4,
               'F': 5,
               'F#': 6,
               'G': 7,
               'G#': 8,
               'A': 9,
               'A#': 10,
               'B': 11
               }

df['key'] = df['key'].map(pitch_class).fillna(-1)

## Create new columns for track's chart classification
def chart_cat(value):
    if value == 0:
        return 'Uncharted'
    elif 1 <= value <= 10:
        return 'Top 10'
    elif 11 <= value <= 50:
        return 'Top 50'
    elif 51 <= value <= 100:
        return 'Top 100'
    elif 101 <= value <= 200:
        return 'Top 200'
    else:
        return 'Charted'

for col_chart in ['in_spotify_charts','in_apple_charts','in_deezer_charts','in_shazam_charts']:
    new_col_chart_name = col_chart + '_category'
    df[new_col_chart_name] = df[col_chart].apply(chart_cat)

df.head()

df['key'] = df['key'].astype('int64')

df.info()t

"""#### **3.2 Descriptive Statistics**"""

df.describe()

"""# **Data Visualization**

# **Most Streamed Songs**
"""

## Sort the data based on the number of streams in descending order
df_sorted = df.sort_values(by='streams', ascending=False)

top_10_streamed = df_sorted.head(10)

## Create a bar chart to visualize the top 10 most streamed songs
plt.subplots(1,1, figsize=(6,4))

sns.barplot(data=top_10_streamed, x='streams', y='track_name')
plt.xlabel('Streams (in billions)', fontsize=7)
plt.ylabel('Track Name', fontsize=7)
plt.xticks(rotation=45, fontsize=7)
plt.yticks(fontsize=7)

plt.show()

"""# **Most streamed artists**

"""

df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

# Grouping by artist(s) again and summing up their streams
artist_streams = df.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head(10)

# Plotting the artists with the most streams again
plt.figure(figsize=(6, 4))
sns.barplot(x=artist_streams.values, y=artist_streams.index, palette="viridis", orient='h')
plt.title('Top 10 Artists Based on Total Streams', fontsize=16)
plt.xlabel('Total Streams (in billions)')
plt.ylabel('Artist(s) Name')
plt.tight_layout()
plt.show()

"""# **Finding Underrated Songs on Spotify**
**Following criterias to be considered for finding underrated songs**
- There should be a limit on streams, to find underrated songs we will have to filter out the popular songs.
- The number of added in playlist should be high, which indicates listeners have liked that song.
- The song shouldn't be on any charts, which indicates the song wasn't discovered through any popular charts, but by word of mouth or exploration.

"""

df[['in_spotify_playlists','streams','in_spotify_charts']].describe()

df.query("streams < 140000000 & in_spotify_charts == 0 & in_spotify_playlists >  2000")

"""### Relationship between Stream Count and other Variables"""

## Create a dataset to only include columns with numeric variables
df_int = df.select_dtypes(include='int64').copy()

## Drop the 'released_month' and 'released_day' columns as we will only analyze the data based on 'released_year'
df_int = df_int.drop(columns=['released_month','released_day'])

df_int.head()

## Plot a histogram to visualize the descriptive statistics of each variable
plt.figure(figsize=(20,25))

for i, col in enumerate(df_int.columns):
    plt.subplot(5,4, i+1)
    sns.histplot(data=df_int, bins=10, x=col, kde=True)
    plt.tight_layout

plt.show()

## Plot a scatterplot to visualize the spread of variables and its relationship to the stream count
plt.figure(figsize=(25,20))

int_no_stream = [col for col in df_int.columns
                   if col != 'streams']

for i, col in enumerate(int_no_stream):
    plt.subplot(5,4, i+1)
    sns.scatterplot(data=df_int, x=col, y='streams')

plt.tight_layout()
plt.show()

## Create a boxplot for total stream duration vs chart placement category
fig, ax = plt.subplots(1,4, figsize=(20,5))

sns.set(font_scale = 0.9)
custom_order = ['Uncharted','Top 10','Top 50','Top 100','Top 200','Charted']

## For Spotify charts
sns.boxplot(data=df, x='streams', y='in_spotify_charts_category', order=custom_order, palette=sns.color_palette('hls'), width=0.3, fliersize=2, ax=ax[0])
ax[0].legend([])
ax[0].set_xlabel(xlabel='total stream duration')
## For Apple charts
sns.boxplot(data=df, x='streams', y='in_apple_charts_category', order=custom_order, palette=sns.color_palette('hls'), width=0.3, fliersize=2, ax=ax[1])
ax[1].legend([])
ax[1].set_xlabel(xlabel='total stream duration')
## For Deezer charts
sns.boxplot(data=df, x='streams', y='in_deezer_charts_category', order=custom_order, palette=sns.color_palette('hls'), width=0.3, fliersize=2, ax=ax[2])
ax[2].legend([])
ax[2].set_xlabel(xlabel='total stream duration')
## For Shazam charts
sns.boxplot(data=df, x='streams', y='in_shazam_charts_category', order=custom_order, palette=sns.color_palette('hls'), width=0.3, fliersize=2, ax=ax[3])
ax[3].legend([])
ax[3].set_xlabel(xlabel='total stream duration')

plt.tight_layout()
plt.show()

"""### Correlation Matrix

After checking the histograms, scatterplots, and boxplots for the relationship between variables and stream count, we will plot a heatmap correlating variables that could have high correlation to the number of streams.
"""

## Plot a correlation matrix
col_to_corr = ['artist_count','released_year','in_spotify_playlists','in_spotify_charts','streams','in_apple_playlists','in_apple_charts','in_deezer_playlists','in_deezer_charts',
               'in_shazam_charts','danceability_%','valence_%','energy_%','acousticness_%','instrumentalness_%','liveness_%','speechiness_%']

corr_matrix = df_int[col_to_corr].corr()
mask = np.triu(corr_matrix, k=1)
mask = mask | (corr_matrix >= 0.5)

plt.figure(figsize=(12,10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', square=True, mask=~mask, cmap='coolwarm')
sns.set(font_scale=0.7)

plt.show()

"""###  Analysis of the Distribution of Track Metrics per Year of Release

####  **Danceability**
"""

## Create a boxplot
plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='danceability_%', width=0.4, fliersize=2)
plt.xticks(rotation=45, fontsize=8)

plt.show()

"""#### **Valence**"""

## Create a boxplot
plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='valence_%', width=0.4, fliersize=2)
plt.xticks(rotation=45, fontsize=8)

plt.show()

"""#### **Energy**"""

## Create a boxplot
plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='energy_%', width=0.4, fliersize=2)
plt.xticks(rotation=45, fontsize=8)

plt.show()

"""#### **Acousticness**"""

## Create a boxplot
plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='acousticness_%', width=0.4, fliersize=2)
plt.xticks(rotation=45, fontsize=8)

plt.show()

"""#### **Instrumentalness**"""

## Create a boxplot
plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='instrumentalness_%', width=0.4, fliersize=2)
plt.xticks(rotation=45, fontsize=8)

plt.show()

"""#### **Liveness**"""

plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='liveness_%', width=0.4, fliersize=2)
plt.xticks(rotation=45)

plt.show()

"""#### **Speechiness**"""

plt.subplots(1,1, figsize=(15,3))

sns.boxplot(data=df, x='released_year', y='speechiness_%', width=0.4, fliersize=2)
plt.xticks(rotation=45)

plt.show()

"""###Distribution of Top Streamed Tracks in other Platforms

#### **Based on Platform Charts**
"""

## Plot a count plot to visualize the number of tracks present or not present in the charts of both platforms

fig, axes = plt.subplots(2,3, figsize=(10,6))

## For tracks in both Spotify and Apple charts
df['both_spotify_apple_charts'] = (df['in_spotify_charts'] > 0) & (df['in_apple_charts'] > 0)
sns.countplot(data=df, x='both_spotify_apple_charts', width=0.4, ax=axes[0,0])
axes[0,0].set_xticklabels(['Not in both','Present in both'])
axes[0,0].set_xlabel(xlabel='Both in Spotify and Apple Charts')

## For tracks in both Spotify and Deezer charts
df['both_spotify_deezer_charts'] = (df['in_spotify_charts'] > 0) & (df['in_deezer_charts'] > 0)
sns.countplot(data=df, x='both_spotify_deezer_charts', width=0.4, ax=axes[0,1])
axes[0,1].set_xticklabels(['Not in both','Present in both'])
axes[0,1].set_xlabel(xlabel='Both in Spotify and Deezer Charts')

## For tracks in both Spotify and Shazam charts
df['both_spotify_shazam_charts'] = (df['in_spotify_charts'] > 0) & (df['in_shazam_charts'] > 0)
sns.countplot(data=df, x='both_spotify_shazam_charts', width=0.4, ax=axes[0,2])
axes[0,2].set_xticklabels(['Not in both','Present in both'])
axes[0,2].set_xlabel(xlabel='Both in Spotify and Shazam Charts')

## For tracks in both Apple and Deezer charts
df['both_apple_deezer_charts'] = (df['in_apple_charts'] > 0) & (df['in_deezer_charts'] > 0)
sns.countplot(data=df, x='both_apple_deezer_charts', width=0.4, ax=axes[1,0])
axes[1,0].set_xticklabels(['Not in both','Present in both'])
axes[1,0].set_xlabel(xlabel='Both in Apple and Deezer Charts')

## For tracks in both Apple and Shazam charts
df['both_apple_shazam_charts'] = (df['in_apple_charts'] > 0) & (df['in_shazam_charts'] > 0)
sns.countplot(data=df, x='both_apple_shazam_charts', width=0.4, ax=axes[1,1])
axes[1,1].set_xticklabels(['Not in both','Present in both'])
axes[1,1].set_xlabel(xlabel='Both in Apple and Shazam Charts')

## For tracks in both Deezer and Shazam charts
df['both_deezer_shazam_charts'] = (df['in_deezer_charts'] > 0) & (df['in_shazam_charts'] > 0)
sns.countplot(data=df, x='both_deezer_shazam_charts', width=0.4, ax=axes[1,2])
axes[1,2].set_xticklabels(['Not in both','Present in both'])
axes[1,2].set_xlabel(xlabel='Both in Deezer and Shazam Charts')

plt.tight_layout()
plt.show()

## Determine the correlation values between two platforms
platforms_chart = ['Spotify','Apple','Deezer','Shazam']
platforms_chart_comb = [(platforms_chart[i], platforms_chart[j]) for i in range(3) for j in range(i + 1, 4)]

for i, (platform1, platform2) in enumerate(platforms_chart_comb):
    col1 = f'in_{platform1.lower()}_charts'
    col2 = f'in_{platform2.lower()}_charts'

    platform_corr = df[col1].corr(df[col2])

    print(f'Correlation between {platform1} and {platform2}: {platform_corr:.2f}')

"""- The charts above show that top streamed tracks for different platform varies, as the number of tracks that are both present or not present on either platform have varying results for different combinations, with almost considerable amount of tracks that are not present in both platforms.
- The correlation also shows a moderate to low correlation between these variables.

#### **Based on Platform Playlists**
"""

## Plot a count plot to visualize the number of tracks present or not present in the charts of both platforms

fig, ax = plt.subplots(1,3, figsize=(10,3))

## For tracks in both Spotify and Apple playlists
df['both_spotify_apple_playlists'] = (df['in_spotify_playlists'] > 0) & (df['in_apple_playlists'] > 0)
sns.countplot(data=df, x='both_spotify_apple_playlists', width=0.4, ax=ax[0])
ax[0].set_xticklabels(['Not in both','Present in both'])
ax[0].set_xlabel(xlabel='Both in Spotify and Apple Playlists')

## For tracks in both Spotify and Deezer playlists
df['both_spotify_deezer_playlists'] = (df['in_spotify_playlists'] > 0) & (df['in_deezer_playlists'] > 0)
sns.countplot(data=df, x='both_spotify_deezer_playlists', width=0.4, ax=ax[1])
ax[1].set_xticklabels(['Not in both','Present in both'])
ax[1].set_xlabel(xlabel='Both in Spotify and Deezer Playlists')

## For tracks in both Apple and Deezer charts
df['both_apple_deezer_playlists'] = (df['in_apple_playlists'] > 0) & (df['in_deezer_playlists'] > 0)
sns.countplot(data=df, x='both_apple_deezer_charts', width=0.4, ax=ax[2])
ax[2].set_xticklabels(['Not in both','Present in both'])
ax[2].set_xlabel(xlabel='Both in Apple and Deezer')

plt.tight_layout()
plt.show()

## Determine the correlation values between two platforms
platforms_playlist = ['Spotify','Apple','Deezer']
platforms_playlist_comb = [(platforms_playlist[i], platforms_playlist[j]) for i in range(3) for j in range(i + 1, 3)]

for i, (platform1, platform2) in enumerate(platforms_playlist_comb):
    col1a = f'in_{platform1.lower()}_playlists'
    col2a = f'in_{platform2.lower()}_playlists'

    platform_corr = df[col1a].corr(df[col2a])

    print(f'Correlation between {platform1} and {platform2}: {platform_corr:.2f}')

"""- Majority of songs in the top streamed tracks that are present in Spotify playlists are also present in Apple and Deezer playlists.
- The chart results is backed by a high correlation score for Spotify and Apple playlists (0.71) and Spotify and Deezer playlists (0.83).

### Chart Performance based on Track Metrics

#### **Danceability**
"""

platforms = ['Spotify','Apple','Deezer','Shazam']

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, y=f'in_{platform.lower()}_charts_category', x='danceability_%', order=custom_order, ax=axes[i], orient='h', width=0.4, palette=sns.color_palette('hls'))

plt.tight_layout()
plt.show()

"""#### **Valence**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='valence_%', y=f'in_{platform.lower()}_charts_category', order=custom_order, ax=axes[i], palette=sns.color_palette('hls'), width=0.4)

plt.tight_layout()
plt.show()

"""#### **Energy**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='energy_%', y=f'in_{platform.lower()}_charts_category', order=custom_order, ax=axes[i], palette=sns.color_palette('hls'), width=0.4)

plt.tight_layout()
plt.show()

"""#### **Acousticness**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='acousticness_%', y=f'in_{platform.lower()}_charts_category', ax=axes[i], order=custom_order, width=0.4, palette=sns.color_palette('hls'))

plt.tight_layout()
plt.show()

"""#### **Instrumentalness**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='instrumentalness_%', y=f'in_{platform.lower()}_charts_category', width=0.4, palette=sns.color_palette('hls'), order=custom_order, ax=axes[i])

plt.tight_layout()
plt.show()

"""#### **Liveness**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='liveness_%', y=f'in_{platform.lower()}_charts_category', order=custom_order, width=0.4, palette=sns.color_palette('hls'), ax=axes[i])

plt.tight_layout()
plt.show()

"""#### **Speechiness**"""

fig, axes = plt.subplots(1,4, figsize=(16,3))

for i, platform in enumerate(platforms):
    sns.boxplot(data=df, x='speechiness_%', y=f'in_{platform.lower()}_charts_category', width=0.4, order=custom_order, palette=sns.color_palette('hls'), ax=axes[i])

plt.tight_layout()
plt.show()

"""Analysing most popular songs"""

df['in_deezer_playlists'] = pd.to_numeric(df['in_deezer_playlists'], errors='coerce')
df['in_deezer_playlists'].fillna(0,inplace=True)

df['in_total_playlist'] = df['in_spotify_playlists'] + df['in_apple_playlists'] + df['in_deezer_playlists']

df2 = df.sort_values(by=['streams'],ascending=False)
df2 = df2.head(500)

df2['VED'] = df2['danceability_%'] + df2['valence_%'] + df2['energy_%']

sns.set_theme(style="white")

sns.relplot(x="VED", y="streams", hue="key", size="in_total_playlist",
            sizes=(40, 400), alpha=.7,palette = 'muted',
            height=6, data=df2)

plt.title('Analysing top 500 streamed songs', fontsize=15)
plt.xlabel('VED (Valence + Energy + Danceability)')
plt.ylabel('Streams')
plt.show()