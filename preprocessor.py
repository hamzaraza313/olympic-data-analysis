import  pandas as pd
import numpy as np


def preprocess(df,region_df):
    # filter for summer olympics
    df = df[df['Season'] == 'Summer']
    # Merge with region_df
    df = df.merge(region_df, on= 'NOC' , how= 'left')
    # Drop duplicates
    df.drop_duplicates(inplace= True)
    # Medal OneHot Encoding
    df = pd.concat([df , pd.get_dummies(df['Medal'])],axis=1)

    return df


def fetch_medal_tally(df,country,year):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if 'Country' == 'Overall' and  'Year' == 'Overall':
        temp_df = medal_df
    if 'Country' != 'Overall' and 'Year' == 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if 'Country' == 'Overall' and 'Year' != 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if 'Country' != 'Overall' and 'Year' != 'Overall':
        temp_df = medal_df[medal_df['region'] == country and medal_df['Year'] == int(year)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else :
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

