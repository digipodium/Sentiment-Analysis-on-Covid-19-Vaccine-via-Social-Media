import streamlit as st

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from database import Report
from visualization import *
from AnalyseData import Analyse

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()


# analysis = Analyse("datasets/vaccination_tweets.csv")
analysis = Analyse("datasets/vaccination_all_tweets.csv")

st.title('Sentiment Analysis on Covid-19 Vaccine via Social Media')
st.text("")
st.text("")

st.image('logo.jpg', use_column_width=True)
st.markdown("---")
sidebar = st.sidebar
sidebar.title('Sentiment Analysis on Covid-19 Vaccine via Social Media')
sidebar.markdown("---")


def viewDataset():
    st.header('Data Used in Project')
    dataframe = analysis.getDataframe()

    with st.spinner("Loading Data..."):
        st.dataframe(dataframe[:5000])

        st.markdown('---')
        cols = st.beta_columns(4)
        cols[0].markdown("### No. of Rows :")
        cols[1].markdown(f"# {dataframe.shape[0]}")
        cols[2].markdown("### No. of Columns :")
        cols[3].markdown(f"# {dataframe.shape[1]}")
        st.markdown('---')

        st.header('Summary')
        st.dataframe(dataframe.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical', 'bool': 'Categorical'}
        types = list(map(lambda t: types[str(t)], dataframe.dtypes))
        st.header('Dataset Columns')
        for col, t in zip(dataframe.columns, types):
            st.markdown(f"### {col}")
            cols = st.beta_columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"# {dataframe[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")


def analyseTweets():
    with st.spinner("Loading Data ... "):
        st.header('Twitter Accounts')
        # st.plotly_chart(plotBar(analysis.getDataframe(), 'user_verified', "Verified vs unverified"))
        # st.write(analysis.getDataframe())
        st.plotly_chart(piechart(analysis.getDataframe()),
                        use_container_width=True)
        st.plotly_chart(add_tracePlot(analysis.getDataframe(),),
                        use_container_width=True)
        st.plotly_chart(barplot1(analysis.getDataframe(), 'user_name', 'total_engagement',
                                 'total_engagement', 'Viridis', 'Accounts per Engagements'), use_container_width=True)


def analyseTweets():
    with st.spinner("Loading Analysis..."):
        st.header('Verified vs Unverified Accounts')
        data = analysis.getVerified()
        st.plotly_chart(plotPie(['Unverified Accounts', 'Verified Accounts'], data.values,
                                'Most of the Tweets are from Non-Verified Accounts'), use_container_width=True)

        st.header('Tweet Engagements on the basis of Followers')
        st.plotly_chart(barplot(analysis.getDataframe(), 'acc_class', 'total_engagement',
                                'total_engagement', 'Rainbow', 'Most of the responses are given by popular accounts with huge audience following'), use_container_width=True)

        st.header('Media vs No Media Tweets')
        data = analysis.getDataframe()
        st.plotly_chart(plotPie(['Media', 'No Media'], data.groupby(
            'med').count()['user_name'].values, 'Almost all the Responses contained Media such as Images, Videos, Gifs etc.'), use_container_width=True)

        st.header('Length of Tweets')


def analyseSentiments():
    with st.spinner("Loading Analysis..."):
        st.header('Most Used words in Tweets')
        st.image('plotImages/Cloud1.png', use_column_width=True)

        st.header('Most Used words in Tweets')
        st.image('plotImages/Cloud1_bar.png', use_column_width=True)

        st.header('Most Used words in Tweets')
        st.image('plotImages/Cloud1.png', use_column_width=True)

        st.header('Sentiment Count')
        data = analysis.getPolarityCount()
        st.plotly_chart(plotPie(data.index, data.values,
                                'title'), use_container_width=True)

        st.plotly_chart(barplot(analysis.getEngagementSentiment(
        ), 'total_engagement', 'sentiment', 'total_engagement', 'Rainbow', 'title'), use_container_width=True)


sidebar.header('Choose Your Option')
options = ['View Dataset',
           'Tweets and their account Analysis', 'Sentiment Analysis']
choice = sidebar.selectbox(options=options, label="Choose Action")

with st.spinner("Please Wait for Some Time..."):
    if choice == options[0]:
        viewDataset()
    elif choice == options[1]:
        analyseTweets()
    elif choice == options[2]:
        analyseSentiments()
