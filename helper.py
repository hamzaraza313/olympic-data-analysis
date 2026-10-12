import pandas as pd
import numpy as np


def medal(df):
    # drop duplicates medal count
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    # sort and group by acc to countries
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    # adding a col of Total medals of every country
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return  medal_tally

def select_year_country(df):
    yearlist = df['Year'].unique().tolist()
    yearlist.sort()
    yearlist.insert(0,'Overall')

    countrylist=np.unique(df['region'].dropna()).tolist()
    countrylist.insert(0, 'Overall')

    return yearlist,countrylist

def fetch_medal(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag= 0
    if year == 'Overall' and country == 'Overall' :
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall' :
       flag = 1
       temp_df =  medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall' :
         temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall' :
         temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]
    if flag == 1 :
         x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year'
                                                                                   ).reset_index()
    else :
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return  x


def data_overtime(df,col):
    nations_overtheyears = df.drop_duplicates(['Year', col])['Year'].value_counts().sort_values().reset_index()
    return  nations_overtheyears


def most_medals(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall' :
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().head(15).reset_index()
    x = x.merge(df, on='Name' )[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns=({'count':'Medals'}),inplace=True)
    return x


def countrywise_medals(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['NOC','Team','Games','Year','City','Sport','Event','Medal'],inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    temp_df=temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df

def sports_wise_performance(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['NOC','Team','Games','Year','City','Sport','Event','Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    if temp_df.empty:
        return  pd.DataFrame()
    pt = pd.pivot_table(temp_df,index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_medals_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().head(15).reset_index()
    x = x.merge(df, on='Name' )[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns=({'count':'Medals'}),inplace=True)
    return x
