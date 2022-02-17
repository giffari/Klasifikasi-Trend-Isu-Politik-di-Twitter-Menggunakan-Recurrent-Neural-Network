import os, csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#create stopowrd
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
    
def stemmIndo(text):
    text = stemmer.stem(text)
    text = stopword.remove(text)
    return text

with open('tweets_10000.csv') as t:
    c = csv.reader(t, delimiter=',')
    i = 0
    with open('tweets_10000_stemmed.csv', 'w', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['label', 'created_at', 'tweet_id', 'tweet_text', 'retweet_count', 'favorite_count', 'tweet_lang', 'user_id', 'user_name', 'user_screen_name', 'user_since', 'user_time_zone', 'user_verified'])
        for row in c:
            if i == 0:
                i += 1
            else:
                if row[0] == '0':
                    row[0] = 'negatif'
                elif row[0] == '2':
                    row[0] = 'netral'
                else:
                    row[0] = 'positif'
                
                row[3] = stemmIndo(row[3])
                print(row[3])
                print('')
                writer.writerow(row)
                i += 1