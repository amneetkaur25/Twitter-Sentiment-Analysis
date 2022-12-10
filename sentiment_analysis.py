import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import tweepy
from tweepy import OAuthHandler
import re 
import textblob
from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import seaborn as sns
from matplotlib import pyplot as plt
import json



# To hide warnings
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)
#st.set_page_config(layout="wide")

#selected=option_menu(menu_title=None,options=["Home","Analysis"],orientation="horizontal",icons=['house','book'])

STYLE =st.markdown( """
<style>
div.stButton > button:first-child{
    background-color: #56a0d3;
    color:#ffffff;
    border: 2px solid red;
    height: 50px;
    width: 50%;

}
div.stButton >button:hover {
    background-color:#FF0000;
    color:##ff99ff;
}
}
</style> """,unsafe_allow_html=True)

# function for twitter animation
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)

# function for snow flakes 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("D:\programs\projects\.Streamlit\style.css")
# load animation
animation_symbol="❄"

st.markdown(f""" 
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
<div class="snowflake"> {animation_symbol}</div>
""",unsafe_allow_html=True)

# main function
def main():
    html_temp="""
    <div style="background-color:Red;"><p style="color:white;font-size:40px;padding:10px"> Live Twitter Sentiment Analysis 😊🙂 </p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

     ################# Twitter API Connection #######################
    consumer_key = "HM9PRUHq7jldbHMdLoXFDcx1y"
    consumer_secret = "MnJAx7Kp8IDyW9hPL1wH41Bonp7tSNF1ChUjaMIgQMazsGnpEj"
    access_token = "1598349728252821504-heiEapi16g6rQNc01Nu3RMUIlpSkFI"
    access_token_secret = "f4FQ5R3GkgMbc0Rp4Zo1xEHfGpuFK36DyF1ssCucH83WC"


    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    df=pd.DataFrame(columns=["Date","User","IsVerified","Tweet","Likes","RT","User_location"])
    # Function to extract tweets
    def get_tweets(Topic,Count):
        i=0
        for tweet in tweepy.Cursor(api.search_tweets,q=Topic,lang='en').items():
            print(i,end='/r')
            df.loc[i,'Date']=tweet.created_at
            df.loc[i,'User']=tweet.user.name
            df.loc[i,'IsVerified']=tweet.user.verified
            df.loc[i,'Tweet']=tweet.text
            df.loc[i,'Likes']=tweet.favorite_count
            df.loc[i,'RT']=tweet.retweet_count
            df.loc[i,'User_location']=tweet.user.location
            df.to_csv("TweetDataset.csv")
            i=i+1
            if i>Count:
                break
            else:
                pass
    
    # Function to clean the tweets
    def clean_tweets(tweet):
        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])',' ',str(tweet).lower()).split())

    # function to analyze sentiments 

    def sentiment_analyze(tweet):
        analysis=TextBlob(tweet)
        if analysis.sentiment.polarity>0:
            return 'positive😊'
        elif analysis.sentiment.polarity==0:
            return 'neutral🙂'
        else:
            return 'negative😑'

    # Function to preprocess data for wordcloud

    def prepcloud(Topic_text,Topic):
        Topic=str(Topic).lower()
        Topic=' '.join(re.sub('[^0-9A-Za-z \t]',' ',Topic).split())
        Topic=re.split("\s+",str(Topic))
        stopwords=set(STOPWORDS)
        stopwords.update('Topic') #Add our topic in Stopwords, so it doesnt appear in wordCloud

        text_new=" ".join(txt for txt in Topic_text.split() if txt not in stopwords)
        return text_new

    # function to extract tweets from twitter handle
    df1=pd.DataFrame(columns=["Date","author","twitter_name","Tweet","Likes","RT"])
    def get_tweets_from_user(twitter_user_name, count_tweet=200):
        i=0
        for tweet in tweepy.Cursor(api.user_timeline,screen_name=twitter_user_name,count=count_tweet ).items():
            print(i,end='/r')
            df1.loc[i,'Date']=tweet.created_at
            df1.loc[i,'author']=tweet.user.name
            df1.loc[i,'twitter_name']=tweet.user.screen_name
            df1.loc[i,'Tweet']=tweet.text
            df1.loc[i,'Likes']=tweet.favorite_count
            df1.loc[i,'RT']=tweet.retweet_count
            df1.to_csv("TweetDataset.csv")
            i=i+1
            if i>count_tweet:
                break
            else:
                pass

    # animation picture
    coding=load_lottiefile(r'D:\programs\projects\.Streamlit\twitter-icon1.json')
    st_lottie(coding,height=400)

    # sentence -level analysis
    st.subheader("Sentence-Level Analysis:")
    text=str(st.text_input("Enter a Sentence"))
    blob = TextBlob(text)
    if blob.sentiment.polarity > 0:
        text_sentiment = "Positive😊"
    elif blob.sentiment.polarity == 0:
        text_sentiment = "Neutral🙂"
    else:
        text_sentiment = "Negative😑"
    if len(text)>0:
        st.write("Sentiment is : {}".format(text_sentiment))
    
    
    # collect input from user  :
    st.subheader("Select a 'Topic' or '# hashtag'  which you'd like to get the sentiment analysis on:")
    Topic=str(st.text_input("Enter the Topic you are interseted in (Press Enter once done)"))
    if len(Topic)>0:

        # call the function to extract the data
        with st.spinner("Please wait Tweets are being extracted"):
            get_tweets(Topic,Count=200)
            st.success("Tweets have been Extracted !!!")

        #call the function to get clean tweets
        df['Clean Tweets']=df['Tweet'].apply(lambda x:clean_tweets(x))

        #call the function to analyze tweets
        df['Sentiment']=df['Tweet'].apply(lambda x: sentiment_analyze(x))

        # Overall Summary

        st.write("Total tweets extracted for topic: {}: are:{}".format(Topic,len(df['Tweet'])))
        st.write("Total Positive Tweets are:{}".format(len(df[df['Sentiment']=='positive😊'])))
        st.write("Total Neutral Tweets are:{}".format(len(df[df['Sentiment']=='neutral🙂'])))
        st.write("Total Negative Tweets are:{}".format(len(df[df['Sentiment']=='negative😑'])))

        # see the Extracted data
        if st.button("See the Extracted Data for {}:".format(Topic)):
            st.success("Below is the Extracted Data")
            st.write(df.head(50))

        # get the count plot
        if st.button('Get Count Plot for Different Sentiments'):
            st.success("Generating a Count Plot")
            st.subheader("Count Plot for Different Sentiments")
            st.write(sns.countplot(x=df['Sentiment']))
            st.pyplot()

        # pie chart
        if st.button("Get Pie Chart for Different Sentiments"):
            st.success("Generating a Pie Chart")
            a=len(df[df['Sentiment']=='positive😊'])
            b=len(df[df['Sentiment']=='negative😑'])
            c=len(df[df['Sentiment']=='neutral🙂'])
            d=np.array([a,b,c])
            explode=(0.1,0.1,0.1)
            st.write(plt.pie(d,labels=['Positive','Negative','Neutral'],shadow=True,autopct='%1.2f%%',explode=explode))
            st.pyplot()

        # get the countplot based on verfied and unverified users
        if st.button("Get Count Plot Based on Verified and Unverified Users"):
            st.success("Generating Count Plot (Verified and Unverified Users)")
            st.subheader("Count Plot for different Sentiments for Verified and Unverified Users")
            st.write(sns.countplot(x=df['Sentiment'],hue=df['IsVerified']))
            st.pyplot()

        # Create Wordcloud
        if st.button("Get Word Cloud for all things said about {}".format(Topic)):
            st.success("Generating a WordCloud for all things said about {}".format(Topic))
            text=" ".join(review for review in df['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()

        # WordCloud for Positive Tweets only
        if st.button("Get Word Cloud for all Positive Tweets about {}".format(Topic)):
            st.success("Generating a WordCloud for all Positive Tweets about {}".format(Topic))
            text=" ".join(review for review in df[df['Sentiment']=='positive😊']['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()

        # Wordcloud for all Neagtive Tweets
        if st.button("Get Word Cloud for all Negative Tweets about {}".format(Topic)):
            st.success("Generating a WordCloud for all Negative Tweets about {}".format(Topic))
            text=" ".join(review for review in df[df['Sentiment']=='negative😑']['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()        

    st.subheader("Select a 'Twitter Handle' on whom tweets you'd like to get the sentiment analysis on:")
    Topic=str(st.text_input("Enter the Twitter handle (Press Enter once done)"))
    if len(Topic)>0:
        # call the function to extract the data
        with st.spinner("Please wait Tweets are being extracted"):
            get_tweets_from_user(Topic)
        st.success("Tweets have been Extracted !!!")
        #call the function to get clean tweets
        df1['Clean Tweets']=df1['Tweet'].apply(lambda x:clean_tweets(x))

        #call the function to analyze tweets
        df1['Sentiment']=df1['Tweet'].apply(lambda x: sentiment_analyze(x))

        # Overall Summary

        st.write("Total tweets extracted for twitter handle: {}: are:{}".format(Topic,len(df1['Tweet'])))
        st.write("Total Positive Tweets are:{}".format(len(df1[df1['Sentiment']=='positive😊'])))
        st.write("Total Neutral Tweets are:{}".format(len(df1[df1['Sentiment']=='neutral🙂'])))
        st.write("Total Negative Tweets are:{}".format(len(df1[df1['Sentiment']=='negative😑'])))

         # see the Extracted data
        if st.button("See the Extracted Data"):
            st.success("Below is the Extracted Data")
            st.write(df1.head(50))

        # get the count plot
        if st.button('Get Count Plot '):
            st.success("Generating a Count Plot")
            st.subheader("Count Plot for Different Sentiments")
            st.write(sns.countplot(x=df1['Sentiment']))
            st.pyplot()

        if st.button("Get Pie Chart"):
            st.success("Generating a Pie Chart")
            a=len(df1[df1['Sentiment']=='positive😊'])
            b=len(df1[df1['Sentiment']=='negative😑'])
            c=len(df1[df1['Sentiment']=='neutral🙂'])
            d=np.array([a,b,c])
            explode=(0.1,0.1,0.1)
            st.write(plt.pie(d,labels=['Positive','Negative','Neutral'],shadow=True,autopct='%1.2f%%',explode=explode))
            st.pyplot()

         # Create Wordcloud
        if st.button("Get Word Cloud"):
            st.success("Generating a Word Cloud")
            text=" ".join(review for review in df1['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()

        # WordCloud for Positive Tweets only
        if st.button("Get Word Cloud for all Positive Tweets"):
            st.success("Generating a WordCloud for all Positive Tweets")
            text=" ".join(review for review in df1[df1['Sentiment']=='positive😊']['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()

        # Wordcloud for all Neagtive Tweets
        if st.button("Get Word Cloud for all Negative Tweets "):
            st.success("Generating a WordCloud for all Negative Tweets")
            text=" ".join(review for review in df1[df1['Sentiment']=='negative😑']['Clean Tweets'])
            stopwords=set(STOPWORDS)
            text_newALL=prepcloud(text,Topic)
            wordcloud=WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)
            st.write(plt.imshow(wordcloud,interpolation='bilinear'))
            plt.axis("off")
            st.pyplot()        
    if st.button("Exit"):
        st.balloons()

if __name__=='__main__':
    main()