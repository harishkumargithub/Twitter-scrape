import snscrape.modules.twitter as sns
import pandas as pd
import streamlit as st
import pymongo as pym


def Mongo_push(db):
    conn = pym.MongoClient('localhost', 27017)
    data = conn['TwitterData']
    collection = data['TwitterTable']
    collection.insert_one(db)

def search(query, Tweet_count, to_date, from_date):
    content = []
    for i, tweet in enumerate(
            sns.TwitterSearchScraper(query + " until:" + str(to_date) + " since:" + str(from_date)).get_items()):
        if i > Tweet_count - 1:
            break
        else:
            content.append(
            {'Search': query, 'Date': tweet.date, 'ID': tweet.id, 'URL': tweet.url, 'Tweet': tweet.rawContent,
                 'User': tweet.user.username, 'Reply Count': tweet.replyCount, 'Retweet Count': tweet.retweetCount,
                 'Language': tweet.lang, 'Source': tweet.source, 'Like Count': tweet.likeCount})
    content_df = pd.DataFrame(content)
    return content_df


header = st.container()
with header:
    st.title('Twitter Scrapping 🐣\n\n')
    st.write('Welcome to my Project #Twitter Scrapper\n\n')
    # sidebar configuration
    query = st.sidebar.text_input('Enter the reference to be searched: ')
    Tweet_count = st.sidebar.number_input('Enter the number of tweets to be collected:', min_value=1, max_value=1000)
    from_date = st.sidebar.date_input('Select from date')
    to_date = st.sidebar.date_input('Select to date')

    # Sending the input to scrape data from twitter
    if st.sidebar.button(label='Search'):
        df = search(query, Tweet_count, to_date, from_date)
        st.write(df)
        st.download_button(label='Download as CSV', data=df.to_csv(index=False).encode('utf-8'),
                           file_name='Twitter_search.csv')
        st.download_button(label='Download as JSON', data=df.to_json(index=True), file_name='Twitter_search.json')
        data_dict = df.to_dict('list')
        # Function is used to push data to MongoDB
        Mongo_push(data_dict)
        st.write('The following table is a DataFrame which is the result of the search query given by you')
