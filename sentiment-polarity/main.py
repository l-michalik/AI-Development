from textblob import TextBlob
# from newspaper import Article

# url = 'https://www.bbc.com/news/uk-68359434' # negative

# article = Article(url)

# article.download()
# article.parse()
# article.nlp()

# text = article.summary

with open('file.txt', 'r') as file:
    text = file.read()

blob = TextBlob(text)
print(blob)

sentiment = blob.sentiment.polarity
print(sentiment)

