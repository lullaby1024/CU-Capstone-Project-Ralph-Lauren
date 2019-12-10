import pandas as pd
from os.path import dirname, join
from wordcloud import WordCloud, STOPWORDS


def get_wordcloud(df, store):
    comment_words = ' '
    stopwords = set(STOPWORDS)

    for val in df.labels:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        for words in tokens:
            comment_words = comment_words + words + ' '

    wordcloud = WordCloud(width=1200, height=500,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    fname = 'wordcloud_' + store + '.png'
    # save the WordCloud
    wordcloud.to_file(join('../static', fname))


for store in ['ORLANDO FOA', 'LAS VEGAS NORTH', 'LAS VEGAS SOUTH', 'LANCASTER FSC']:
    df = pd.read_csv(join('../data', 'events_' + store + '.csv'))
    get_wordcloud(df, store)