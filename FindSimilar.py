'''
FindSimilar.py

M.Brinkerhoff * UCSC DomainGeneralization * 2023-06-19 (M)
'''

import csv
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download required resources
nltk.download('wordnet')
nltk.download('stopwords')

# Define the input words
input_words = ['part', 'party', 'people', 'king', 'camp', 'team', 'ten', 'tennis', 'turn']

# Load the frequency data from the CSV file
frequency_data = {}
with open('frequency_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        word = row[0]
        frequency = int(row[1])
        frequency_data[word] = frequency

# Initialize WordNet lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to find words with similar sounds
def find_similar_sounds(word):
    synsets = wordnet.synsets(word)
    similar_sounds = []
    for synset in synsets:
        for lemma in synset.lemmas():
            name = lemma.name()
            if name != word and name.isalpha():
                similar_sounds.append(name)
    return similar_sounds

# Function to calculate word frequency from the frequency data
def calculate_frequency(word):
    return frequency_data.get(word.lower(), 0)

# Function to remove stopwords and lemmatize words
def preprocess_word(word):
    word = word.lower()
    if word in stop_words:
        return None
    lemma = lemmatizer.lemmatize(word)
    if lemma in stop_words:
        return None
    return lemma

# Find similar words with similar frequency
similar_words = {}
for word in input_words:
    similar_sounds = find_similar_sounds(word)
    for similar_word in similar_sounds:
        lemma = preprocess_word(similar_word)
        if lemma is not None:
            frequency = calculate_frequency(lemma)
            similar_words[similar_word] = frequency

# Sort the similar words by frequency
sorted_words = sorted(similar_words.items(), key=lambda x: x[1], reverse=True)

# Write similar words and frequencies to a CSV file
output_file = 'similar_words.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Word', 'Frequency'])
    for line_number, (word, frequency) in enumerate(sorted_words, start=1):
        writer.writerow([word, frequency])
        print(f"Processed line {line_number} - Word: {word}\tFrequency: {frequency}")

print(f"Similar words and frequencies written to {output_file}.")
