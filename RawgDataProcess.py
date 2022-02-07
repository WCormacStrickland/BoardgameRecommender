import pandas as pd
import nltk
import re, string, unicodedata
import inflect
from nltk import WordNetLemmatizer, LancasterStemmer
from nltk.corpus import stopwords

myStopwords = stopwords.words('english')
newStopwords = ['none', 'game', '3d', '3dimensional', 'player', 'players', 'one', 'two', 'three']
myStopwords.extend(newStopwords)


class RawgDataProcess:
    def __init__(self, tags):
        self.tags = tags

    def process(self):
        tags = nltk.word_tokenize(self.tags)
        tags = self.remove_non_ascii(tags)
        tags = self.to_lowercase(tags)
        tags = self.remove_punctuation(tags)
        tags = self.remove_numbers(tags)
        tags = self.remove_stopwords(tags)
        tags = self.lemmatize_verbs(tags)
        self.tags = tags

    def get_tags(self):
        return self.tags

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
