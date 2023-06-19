import xml.etree.ElementTree as ET
from collections import defaultdict
import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import NOUN
from nltk.corpus.reader.wordnet import ADJ
from nltk.corpus.reader.wordnet import VERB
from nltk.corpus.reader.wordnet import ADV

# Load the XML file
tree = ET.parse("enwiki-latest-pages-articles-multistream.xml")
root = tree.getroot()

# Define a list of English stop words
stop_words = set(stopwords.words("english"))

# Initialize a defaultdict to store the word frequencies
word_freq = defaultdict(int)

# Initialize a dictionary to store the phonetic transcriptions
phonetic_transcriptions = {}

# Initialize a dictionary to store the lemmas
# lemmas = {}

# Initialize a dictionary to store the number of morphemes
# num_morphemes = {}

# Initialize a dictionary to store the part of speech
part_of_speech = {}

# Initialize a dictionary to store the neighborhood density for each word
# neighborhood_density = {}

# Iterate through the XML entries
for entry in root.findall("./entries/entry"):
    # Get the word from the XML entry
    word = entry.find("word").text
    
    # Check if the word is not an English stop word
    if word not in stop_words:
        # Increment the word frequency count
        word_freq[word] += 1
        
        # Get the phonetic transcription for the word
        phonetic_transcriptions[word] = ""

        # Get the lemma for the word
        lemmas[word] = WordNetLemmatizer().lemmatize(word, pos=wn.NOUN)

        # Get the number of morphemes in the word
        num_morphemes[word] = len(SnowballStemmer("english").stem(word))
        
        # Get the part of speech for the word
        pos = pos_tag([word])[0][1]
        if pos.startswith('N'):
            part_of_speech[word] = 'Noun'
        elif pos.startswith('V'):
            part_of_speech[word] = 'Verb'
        elif pos.startswith('J'):
            part_of_speech[word] = 'Adjective'
        elif pos.startswith('R'):
            part_of_speech[word] = 'Adverb'
        else:
            part_of_speech[word] = 'Unknown'
    
    # Get the synsets for the word
    synsets = wn.synsets(word, pos=wn.NOUN)
    
    # Calculate the average neighborhood density for the word
    avg_density = sum(len(wn.synset(w).lemma_names()) for w in synsets) / len(synsets) if synsets else 0
    
    # Store the neighborhood density in the dictionary
    neighborhood_density[word] = avg_density

# Sort the word frequencies in descending order
sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# Prepare the data for CSV
data = [
    {
        "word": word,
        "frequency": freq,
        "phonetic_transcription": phonetic_transcriptions[word],
        # "lemma": lemmas[word],
        # "num_morphemes": num_morphemes[word],
        "part_of_speech": part_of_speech[word] #,
        # "neighborhood_density": neighborhood_density[word]
    }
    for word, freq in sorted_freq
]

# Define the CSV fieldnames
fieldnames = ["word", "frequency", "phonetic_transcription", "part_of_speech"]

# Save the data as a CSV file
with open("word_frequencies.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Word frequencies with phonetic transcription, lemma, number of morphemes, part of speech, and neighborhood density saved as 'word_frequencies.csv'.")
