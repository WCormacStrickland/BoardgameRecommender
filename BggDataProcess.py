import pandas as pd
import nltk
import re, string, unicodedata
import inflect
from nltk import WordNetLemmatizer, LancasterStemmer
from nltk.corpus import stopwords

myStopwords = stopwords.words('english')
newStopwords = ['none', 'game', '3d', '3dimensional', 'player', 'players', 'one', 'two', 'three']
myStopwords.extend(newStopwords)


class BggDataProcess:
    def __init__(self):
        self.bgg_df = pd.read_csv('bgg_data2.csv')

    def get_tags(self):
        bgg_df = self.bgg_df
        rows_list = []
        for index in bgg_df.index:
            tags = bgg_df.loc[index, 'category'] + bgg_df.loc[index, 'mechanic'] + bgg_df.loc[index, 'family']
            tags = nltk.word_tokenize(tags)
            tags = self.normalize(tags)
            rows_list.append(tags)

        # my_df = pd.DataFrame(rows_list)
        # my_df.to_csv('bgg_data4.csv')

    def remove_non_ascii(self, tags):
        new_tags = []
        for tag in tags:
            new_tag = unicodedata.normalize('NFKD', tag).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_tags.append(new_tag)
        return new_tags

    def to_lowercase(self, tags):
        new_tags = []
        for tag in tags:
            new_tag = tag.lower()
            new_tags.append(new_tag)
        return new_tags

    def remove_punctuation(self, tags):
        new_tags = []
        for tag in tags:
            new_tag = re.sub(r'[^\w\s]', '', tag)
            if new_tag != '':
                new_tags.append(new_tag)
        return new_tags

    def remove_numbers(self, tags):
        p = inflect.engine()
        new_tags = []
        for tag in tags:
            if not tag.isdigit():
                new_tags.append(tag)
        return new_tags

    def remove_stopwords(self, tags):
        new_tags = []
        for tag in tags:
            if tag not in myStopwords:
                new_tags.append(tag)
        return new_tags

    def lemmatize_verbs(self, tags):
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for tag in tags:
            lemma = lemmatizer.lemmatize(tag, pos='v')
            lemmas.append(lemma)
        return lemmas

    def remove_duplicates(self, tags):
        new_tags = list(set(tags))
        return new_tags

    def normalize(self, tags):
        tags = self.remove_non_ascii(tags)
        tags = self.to_lowercase(tags)
        tags = self.remove_punctuation(tags)
        tags = self.remove_numbers(tags)
        tags = self.remove_stopwords(tags)
        tags = self.lemmatize_verbs(tags)
        tags = self.remove_duplicates(tags)
        return tags

if __name__ == "__main__":
    main()