import snscrape.modules.twitter as sns
import pandas as pd
import pymongo as pym
import streamlit as st
import time


# pushing scrapped data to mongo
def pushing_mongo(content_dict):
    conn = pym.MongoClient('localhost', 27017)
    data = conn['TwitterData']
    collection = data['Twitter_Table']
    collection.insert_one(content_dict)


# webpage configuration
st.set_page_config(page_title='Twitter Scrapper', layout='wide')

# Webpage body
Header = st.container()

with Header:
    st.title('Twitter Scrapping 🐣\n\n')
    st.subheader('Welcome to my Project #Twitter Scrapper\n\n')
    st.write(
        'In this data driven world social media data plays a huge role of keeping data updated as it is the main source of commonly used data')
    st.write('This project can be used to project the glimpse of collecting data from major social media Twitter')
    st.write('I am using snscrapper, a python library to scrape the data from Twitter\n\n')

# sidebar configuration
query = st.sidebar.text_input('Enter the reference to be searched: ')
Tweet_count = st.sidebar.number_input('Enter the number of tweets to be collected:', min_value=1, max_value=1000)
from_date = st.sidebar.date_input('Select from date')
to_date = st.sidebar.date_input('Select to date')

# Scrapping data to a list
content = []

for i, tweet in enumerate(
        sns.TwitterSearchScraper(query + " until:" + str(to_date) + " since:" + str(from_date)).get_items()):
    if i > Tweet_count - 1:
        break
    else:
        content.append(
            {'Search': [query, '+', time.ctime, Tweet_count, ' Scraped data from past', to_date - from_date, 'days'],
             'Date': tweet.date, 'ID': tweet.id, 'URL': tweet.url, 'Tweet': tweet.rawContent,
             'User': tweet.user.username, 'Reply Count': tweet.replyCount, 'Retweet Count': tweet.retweetCount,
             'Language': tweet.lang, 'Source': tweet.source, 'Like Count': tweet.likeCount})

# converting list to Dataframe using pandas
content_df = pd.DataFrame(content)

# displaying Dataframe scrapped from above
st.write('The following table is a DataFrame which is the result of the search query given by you')
st.write(content_df)
st.write('The above DataFrame is automatically uploaded to MongoDB server in the background to keep record of the '
         'search history')

# converting list to Dictionary (mongo can only store dictionary or bson data using pymongo)
content_dict = content_df.to_dict('list')

# on_click feature did not work as intended causing the function to automatically call hence if condition is used
if st.button(label='Upload to MongoDB?'):
    pushing_mongo(content_dict)
st.write('\n\nFeel free to download the search result as CSV or JSON\n\n')
st.download_button(label='Download as CSV', data=content_df.to_csv(index=False).encode('utf-8'),
                   file_name='Twitter_search.csv')
st.download_button(label='Download as JSON', data=content_df.to_json(index=True), file_name='Twitter_search''.json')
