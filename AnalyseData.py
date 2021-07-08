import pandas as pd
from datetime import date
from textblob import TextBlob
from wordcloud import WordCloud
import re

class Analyse:

    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.df = self.df[:1000]
        self.cleanData()
        self.generateSentiments()

    def generateSentiments(self):
        tweets = self.df['text']
        features=tweets.values

        processed_features = []

        for sentence in range(0, len(features)):
            # Remove all the Http: urls
            processed_feature = re.sub('(https?://\S+)', '', str(features[sentence]))
            
            # Remove all the special characters
            processed_feature = re.sub(r'\W', ' ', processed_feature)

            # Remove all single characters
            processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

            # Remove single characters from the start
            processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

            # Substituting multiple spaces with single space
            processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

            # Removing prefixed 'b'
            processed_feature = re.sub(r'^b\s+', '', processed_feature)

            # Converting to Lowercase
            processed_feature = processed_feature.lower()

            processed_features.append(processed_feature)

        self.df['Tweets']=processed_features

        self.df['Subjectivity'] = self.df['Tweets'].apply(self.getSubjectivity)
        self.df['Polarity'] = self.df['Tweets'].apply(self.getPolarity)
        self.df['sentiment'] = self.df['Polarity'].apply(self.getAnalysis)
        
    def getPolarityCount(self):
        return self.df.groupby('sentiment').count()['Tweets']

    # Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
    def getAnalysis(self, score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'
        

        # Create a function to get the subjectivity
    def getSubjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity

        # Create a function to get the polarity
    def getPolarity(self, text):
        return  TextBlob(text).sentiment.polarity

    def getEngagementSentiment(self):
        return self.df.groupby('sentiment', as_index=False).agg({'total_engagement': 'sum'})
        

    def cleanData(self):
        self.df['acc_class'] = self.df['user_followers'].apply(lambda x:'weak'if x<=100 else ('norm' if 1000>=x>100 else 
                                                                       ('strong' if 10000>=x>1000
                                                                        else 'influencer')))
        self.df['total_engagement']=self.df['retweets']+self.df['favorites']

        self.df['med'] = self.df['text'].apply(lambda word:word.count('https://t.co/'))
        self.df['med'] = self.df['med'].apply(lambda x:'No Media' if x==0 else 'Media')

        self.df['today']=date.today()
        self.df['user_created']=pd.to_datetime(self.df['user_created']).dt.year
        self.df['today']=pd.to_datetime(self.df['today'])
        self.df['today']=self.df['today'].dt.year
        self.df['acc_age']= self.df['today']-self.df['user_created']

    def getVerified(self):
        return self.df.groupby('user_verified').count()['user_name']

    def getDataframe(self):
        return self.df

    def getMediavsNoMediaCount(self):
        return 

    def getAccountClass(self):
        return self.df['acc_class']

    def getEngagement(self):
        return self.df['total_engagement']

    def getMedia(self):
        return self.df[med]

