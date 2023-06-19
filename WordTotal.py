'''
WordTotal.py

This is a python script that queries the Wikipedia sample corpus from english-corpora.org
and returns a csv file that has removed the English stopwords and lists the frequency of each word.

M. Brinkerhoff * UCSC DomainGeneralization * 2023-06-19 (m)
'''


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from nltk.corpus import cmudict
import csv
import string

# Download necessary resources
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

# File path of the file
file_path = 'text.txt'

# Initialize the POS tagger and pronunciation dictionary
pos_tagger = nltk.pos_tag
pronunciation_dict = cmudict.dict()

# Read the .ttl file
with open(file_path, 'r') as file:
    data = file.read()

# Extract words from the .ttl file
words = word_tokenize(data)

# Tokenize and remove punctuation
translator = str.maketrans('', '', string.punctuation)
words = [word.translate(translator) for word in words]

# Count the frequency of each word
frequency = FreqDist(words)

# Remove stopwords
stopwords = set(stopwords.words('english'))
frequency = {word: count for word, count in frequency.items() if word.lower() not in stopwords}

# Function to convert ARPABET to IPA
def arpabet_to_ipa(pronunciation):
    ipa_pronunciation = []
    for phoneme in pronunciation:
        if phoneme[-1].isdigit():
            phoneme = phoneme[:-1]
        ipa_pronunciation.append(phoneme)
    return ipa_pronunciation

# Retrieve the POS tag and pronunciation of each word
pos_tags = []
pronunciations = []

for word in words:
    pos_tag = pos_tagger([word])[0][1]
    pronunciation = pronunciation_dict.get(word.lower(), [[]])[0]

    pos_tags.append(pos_tag)
    pronunciations.append(pronunciation)

# Convert pronunciations to IPA
pronunciations_ipa = [arpabet_to_ipa(pronunciation) for pronunciation in pronunciations]

# Export the result as a CSV file
output_file = 'word_info.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Word', 'POS', 'Pronunciation (IPA)', 'Frequency'])
    for word, count in frequency.items():
        pos_tag = pos_tags[words.index(word)]
        pronunciation = " ".join(pronunciations_ipa[words.index(word)])
        writer.writerow([word, pos_tag, pronunciation, count])

print(f"The results have been exported to {output_file}.")
