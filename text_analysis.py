''' Extract textual data articles from the given URL and perform text analysis to compute variables that are explained below. 
'''
from sys import exception
# import libraries
try:
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    import requests
    from lxml import etree
    session = requests.Session()
    import nltk
    import os
    import string
    import re
    string.punctuation
except ImportError as ie:
    print("It cannot import module and submodule", ie)
my_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}

# Read the Dictionary & make a set
try:
    stopwords_ = 'StopWords'
    stop_words = set()
    for files in os.listdir(stopwords_):
      with open(os.path.join(stopwords_,files),'r',encoding='ISO-8859-1') as f:
        stop_words.update(set(f.read().splitlines()))

    file = open("MasterDictionary\positive-words.txt","r")
    positive_words = set()
    positive_words.update(file.read().splitlines())

    file_1 =open("negative-words.txt","r")
    negative_words = set()
    negative_words.update(file_1.read().splitlines())
except exception as ie:
    print("It can not read word libraries",ie)
# Data cleaning
def preprocess_words(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if len(i.strip()) > 1:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)
    text = y[:]
    return text
# Cleaned word count
def preprocess_words_len(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if len(i.strip()) > 1:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)
    return len(y)
# positive score
def positive_score(text):
    text = preprocess_words(text)
    y = []
    for i in text:
        if i in positive_words:
            y.append(i)
    return len(y)
# Negative score
def negative_score(text):
    text = preprocess_words(text)
    y = []
    for i in text:
        if i in negative_words:
            y.append(i)
    return len(y)
# polarity score
def polarity_score(text):
    return (positive_score(text) - negative_score(text)) / ((positive_score(text) + negative_score(text)) + 0.000001)
# Subjectivity score
def subjectivity_score(text):
    return (positive_score(text) + negative_score(text))/ ((preprocess_words_len(text)) + 0.000001)
# Total num of sentences
def sentence_len(text):
    text = text.lower()
    text = nltk.sent_tokenize(text)
    return len(text)
# Average sentence length
def avg_sentence_len(text):
    return (preprocess_words_len(text))/(sentence_len(text))
# Total Complex word
def complex_word_count(text):
    text = preprocess_words(text)
    y =[]
    vowels ='aeiou'
    for i in text:
        final = [each for each in i.lower() if each in vowels]
        if i.endswith('es') or i.endswith('ed'):
            pass
        elif len(final) >2 :
            y.append(i)
    return len(y)
# Percentage of complex word
def percentage_of_complex_word(text):
    return (complex_word_count(text))/(preprocess_words_len(text))
# Calculate Fog index
def fog_index(text):
    return (0.4) * (avg_sentence_len(text) + percentage_of_complex_word(text))
# Syllable word
def syllable_word(text):
    text = preprocess_words(text)
    y=[]
    vowels ='aeiou'
    for i in text:
        final = [each for each in i.lower() if each in vowels]
        if i.endswith('es') or i.endswith('ed'):
            pass
        elif len(final) >= 1:
            y.append(i)
    return y
# Syllable Count
def syllable_per_word(text):
    text = syllable_word(text)
    vowels ='aeiou'
    y =[]
    n = len(text)
    for i in text:
        a = len(i)
        vow = [each for each in i.lower() if each in vowels]
        b = len(vow)
        y.append(b/a)
    avg = sum(y)/n
    return avg
# Average word length
def avg_word_length(text):
    text = preprocess_words(text)
    length = sum(len(i) for i in text)
    awl = length / len(text)
    return awl
# Personal Pronouns
def personal_pronouns(text):
    pattern = r"\b(I|we|my|ours|us)\b"   # pattern to check if those words exists
    pattern = r"(?<!\bUS\b)" + pattern   # pattern should not include US instead of us
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    count = len(matches)
    return count
dict = {
    'URL_ID': [],
    'URL': [],
    'PositiveScore': [],
    'Negative Score' : [],
    'POLARITY SCORE': [],
    'SUBJECTIVITY SCORE' : [],
    'AVG SENTENCE LENGTH' : [],
    'PERCENTAGE OF COMPLEX WORDS' : [],
    'FOG INDEX' : [],
    'COMPLEX WORD COUNT' : [],
    'WORD COUNT' : [],
    'SYLLABLE PER WORD' : [],
    'PERSONAL PRONOUNS' : [],
    'AVG WORD LENGTH' : []
}

df = pd.read_excel('Input.xlsx')
for ind in df.index:
    response = session.get(df['URL'][ind],headers=my_headers)
    soup = BeautifulSoup(response.content, "html.parser")
    Article = []
    try:
        Article.append(soup.find('h1').get_text())
        article = soup.find_all('p')
    except Exception as ie:
        print("does't extract data",ie)
    for i in article:
        Article.append(i.get_text())
    text = ". ".join(Article)
    pstvscr = positive_score(text)
    ngtvscr = negative_score(text)
    poltscr = polarity_score(text)
    subtscr = subjectivity_score(text)
    avgsenlnt = avg_sentence_len(text)
    percomwrd = percentage_of_complex_word(text)
    fgind = fog_index(text)
    comwrd = complex_word_count(text)
    wrd = preprocess_words_len(text)
    sylperwrd = syllable_per_word(text)
    perpro = personal_pronouns(text)
    avgwrdlnt = avg_word_length(text)

    Article.clear()
    dict['URL_ID'].append(df["URL_ID"][ind])
    dict['URL'].append(df["URL"][ind])
    dict['PositiveScore'].append(pstvscr)
    dict['Negative Score'].append(ngtvscr)
    dict['POLARITY SCORE'].append(poltscr)
    dict['SUBJECTIVITY SCORE'].append(subtscr)
    dict['AVG SENTENCE LENGTH'].append(avgsenlnt)
    dict['PERCENTAGE OF COMPLEX WORDS'].append(percomwrd)
    dict['FOG INDEX'].append(fgind)
    dict['COMPLEX WORD COUNT'].append(comwrd)
    dict['WORD COUNT'].append(wrd)
    dict['SYLLABLE PER WORD'].append(sylperwrd)
    dict['PERSONAL PRONOUNS'].append(perpro)
    dict['AVG WORD LENGTH'].append(avgwrdlnt)

newDf = pd.DataFrame(dict)
newDf.to_csv('Extraction_and_sentiment_analysis.csv')
