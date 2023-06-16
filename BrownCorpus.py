'''
BrownCorpus.py

This is a python script that queries the Brown Corpus and returns the frequency of the 
frequency of the first word as a csv file that has removed the English stopwords.

M. Brinkerhoff * UCSC DomainGeneralization * 2023-05-31 (W)
'''

import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.corpus import cmudict
import csv
import string

# Download the Brown Corpus, stopwords, POS tagger, and pronunciation dictionary
nltk.download('brown')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

# Load the Brown Corpus
sentences = brown.sents()

# Initialize the POS tagger and pronunciation dictionary
pos_tagger = nltk.pos_tag
pronunciation_dict = cmudict.dict()

# Retrieve the first word, POS tag, and pronunciation of each sentence
first_words = []
pos_tags = []
pronunciations = []

for sentence in sentences:
    if len(sentence) > 0:
        first_word = sentence[0]
        pos_tag = pos_tagger([first_word])[0][1]
        pronunciation = pronunciation_dict.get(first_word.lower(), [[]])[0]

        first_words.append(first_word)
        pos_tags.append(pos_tag)
        pronunciations.append(pronunciation)

# Tokenize and remove punctuation
translator = str.maketrans('', '', string.punctuation)
first_words = [word.translate(translator) for word in first_words]

# Count the frequency of each first word
frequency = FreqDist(first_words)

# Remove stopwords
stopwords = set(stopwords.words('english'))
frequency = {word: count for word, count in frequency.items() if word.lower() not in stopwords}

# Export the result as a CSV file
output_file = 'first_word_info.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['First Word', 'POS', 'Pronunciation', 'Frequency'])
    for word, count in frequency.items():
        pos_tag = pos_tags[first_words.index(word)]
        pronunciation = " ".join(pronunciations[first_words.index(word)])
        writer.writerow([word, pos_tag, pronunciation, count])

print(f"The results have been exported to {output_file}.")