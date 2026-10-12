import streamlit as st
import preprocessor
import helper
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df_globe = preprocessor.preprocess(df, region_df)
st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/79484a71-9188-4973-b391-05510394986e/dc4gca6-6d8c30f8-bf41-4ec7-b5e2-5f019ef572c9.jpg/v1/fill/w_1192,h_670,q_70,strp/olympic_rings_by_mardoek50_dc4gca6-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTA4MCIsInBhdGgiOiJcL2ZcLzc5NDg0YTcxLTkxODgtNDk3My1iMzkxLTA1NTEwMzk0OTg2ZVwvZGM0Z2NhNi02ZDhjMzBmOC1iZjQxLTRlYzctYjVlMi01ZjAxOWVmNTcyYzkuanBnIiwid2lkdGgiOiI8PTE5MjAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.VMBophxMd86Grt4FHa8uExgYicRrczYgbXFlXKQ1OSc')
side_menu = st.sidebar.radio(
    'Select an Option' ,
    ('Medal Tally' , 'Overall Analysis' , 'Country-Wise Analysis'),
    )

if side_menu == 'Medal Tally':
    st.sidebar.subheader('Medal Tally')
    years,country = helper.select_year_country(df_globe)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)

    medal_tally = helper.fetch_medal(df_globe,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall' :
        st.title('Overall Medal Tally')
    if selected_year != 'Overall' and selected_country == 'Overall' :
        st.title(f'Medal Tally in {selected_year}')
    if selected_year == 'Overall' and selected_country != 'Overall' :
        st.title(f'Medal Tally of {selected_country}')
    if selected_year != 'Overall' and selected_country != 'Overall' :
        st.title(f'Medal Tally of {selected_country} in {selected_year}')
    st.table(medal_tally)

if side_menu == 'Overall Analysis' :
    editions = df_globe['Year'].unique().shape[0] - 1
    cities = df_globe['City'].unique().shape[0]
    sports = df_globe['Sport'].unique().shape[0]
    events = df_globe['Event'].unique().shape[0]
    athletes = df_globe['Name'].unique().shape[0]
    countries = df_globe['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2 , col3  = st.columns(3)
    with col1:
        st.header('Editions')
        st.subheader(editions)
    with col2:
        st.header('Cities')
        st.subheader(cities)
    with col3:
        st.header('Sports')
        st.subheader(sports)

    col4 , col5 , col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.subheader(events)
    with col5:
        st.header('Athletes')
        st.subheader(athletes)
    with col6:
        st.header('Countries')
        st.subheader(countries)


    st.subheader('Number of Nations Over the Years')
    nations_over_the_years = helper.data_overtime(df_globe,'region')
    fig = px.line(nations_over_the_years,x='Year',y='count')
    st.plotly_chart(fig)

    st.subheader('Number of Events Over the Years')
    events_over_the_years = helper.data_overtime(df_globe,'Event')
    fig = px.line(events_over_the_years,x='Year',y='count')
    st.plotly_chart(fig)

    st.subheader('Number of Athletes Over the Years')
    athletes_over_the_years = helper.data_overtime(df_globe,'Name')
    fig=px.line(athletes_over_the_years,x='Year',y='count')
    st.plotly_chart(fig)

    st.subheader('Number of Events Over the Years(Every Sport)')
    ax = plt.figure(figsize = (20,20))
    heat = df_globe.drop_duplicates(subset=['Year','Sport','Event'])
    heat = pd.pivot_table(heat,index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0)
    fig =sns.heatmap(heat,annot=True,cmap='Blues',fmt='g')
    st.pyplot(ax)




    st.subheader('Most Successful Athletes')
    all_sports = df_globe['Sport'].unique().tolist()
    all_sports.sort()
    all_sports.insert(0,'Overall')
    selected_sports = st.selectbox('Select Sport',all_sports)
    success = helper.most_medals(df_globe,selected_sports)
    st.table(success)



if side_menu == 'Country-Wise Analysis' :
    st.sidebar.title('Country Wise Analysis')
    country_list = df_globe['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Region',country_list)
    country = helper.countrywise_medals(df_globe,selected_country)
    st.title(f'{selected_country} Medal Tally Over the Years')
    if country.empty:
        st.markdown('No Medals in Olympics',text_alignment='center')
    else:
        fig = px.line(country,x='Year',y='Medal')
        st.subheader('Line Plot of Medals',text_alignment='center')
        st.plotly_chart(fig)

    pt = helper.sports_wise_performance(df_globe,selected_country)
    if pt.empty:
        st.markdown('No Medals in Olympics',text_alignment='center')
    else :
        heatmap,ht = plt.subplots(figsize = (20,20))
        st.subheader('Heatmap of Sportswise Medals', text_alignment='center')
        ht = sns.heatmap(pt,annot=True)
        st.pyplot(heatmap)


    performance = helper.most_medals_countrywise(df_globe,selected_country)
    st.subheader(f'Most Successful Athletes in {selected_country}',text_alignment='center')
    if performance.empty:
        st.markdown('No Medals in Olympics',text_alignment='center')
    else:
        st.table(performance)

