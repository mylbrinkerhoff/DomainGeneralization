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
from nltk.corpus import reuters
import csv
import string

# Download the Brown Corpus and stopwords
nltk.download('brown')
nltk.download('stopwords')

# Load the Brown Corpus
sentences = brown.sents()

# Retrieve the first word of each sentence
first_words = [sentence[0] for sentence in sentences]

# Tokenize and remove punctuation
translator = str.maketrans('', '', string.punctuation)
first_words = [word.translate(translator) for word in first_words]

# Count the frequency of each first word
frequency = FreqDist(first_words)

# Remove stopwords
# stopwords = set(stopwords.words('english'))
frequency = {word: count for word, count in frequency.items() if word.lower() not in stopwords}

# Export the result as a CSV file
output_file = 'first_word_frequency.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['First Word', 'Frequency'])
    writer.writerows(frequency.items())

print(f"The results have been exported to {output_file}.")