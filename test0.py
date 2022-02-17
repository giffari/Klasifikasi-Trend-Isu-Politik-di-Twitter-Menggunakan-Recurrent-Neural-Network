import os, re
import tweepy as tw
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from sklearn.feature_extraction.text import TfidfVectorizer

os.system("clear")

consumer_key= "3Ys8PPUlCcxqx9uon3cgofeQJ"
consumer_secret= "iBfV9X2nv2PIF77CwH4YE7cISa1LT74iVgpKBDFM1X6daePk9E"
access_token= "892330049675735042-PdnuZ2N0gdCvyGa5cHlGMG5EPQqBM7D"
access_token_secret= "niKYLtUA2UQFxoPuuCVUQ5lfNekOqtYDJe31nwd2iNXVF"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# create stopword list
factory = StopWordRemoverFactory()
stop_factory = StopWordRemoverFactory().get_stop_words()
more_stopword = [] # additional stopword
data = stop_factory + more_stopword # merge stopwords
dictionary = ArrayDictionary(data)
stopwords = StopWordRemover(dictionary)

# cleaning function
def cleaning(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())

# Define the search term and the date_since date as variables
search_words = "politik"
date_since = "2020-07-09"
new_search = search_words + " -filter:retweets"

# Collect tweets
tweets = tw.Cursor(api.search,
                    tweet_mode="extended",
                    q=new_search,
                    lang="id",
                    since=date_since).items(5)

# Iterate and print tweets
# _data = [tweet._json for tweet in tweets]
_text = [tweet.full_text for tweet in tweets]
_document = []
for text in _text:
    param = cleaning(text) # cleaning with regex
    param = param.lower() # case folding
    param = stopwords.remove(param) # stopword removal
    param = param.split() # tokenization
    param = [stemmer.stem(p) for p in param] # stemming
    param = ' '.join(map(str, param)) 
    _document.append(param)

# TFIDF
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(_document)
feature_names = vectorizer.get_feature_names()
dense = vectors.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)
print(df)