import re
import os

TAG_FILES = {
    'Determiner': 'determiners.txt',
    'Noun': 'nouns.txt',
    'Verb': 'verbs.txt',
    'Auxiliary Verb': 'auxiliary.txt',
    'Modal Verb': 'modals.txt',
    'Pronoun': 'pronouns.txt',
    'Adjective': 'adjectives.txt',
    'Adverb': 'adverbs.txt',
    'Preposition': 'prepositions.txt',
    'Conjunction': 'conjunctions.txt',
    'Interjection': 'interjections.txt',
    'Numeral': 'numerals.txt',
    'Punctuation': 'punctuations.txt'
}

# Load all tag wordlists from files once
def load_pos_dict():
    base_path = os.path.join(os.path.dirname(__file__), "pos_tags")
    pos_dict = {}
    for full_tag, filename in TAG_FILES.items():
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        pos_dict[word] = full_tag
    return pos_dict

POS_DICT = load_pos_dict()

def simple_tokenize(sentence):
    return re.findall(r"\w+|[^\w\s]", sentence, re.UNICODE)

def basic_pos_tagger(tokens):
    return [(token, POS_DICT.get(token.lower(), "Unknown")) for token in tokens]

def lexical_analysis(sentence):
    tokens = simple_tokenize(sentence)
    return basic_pos_tagger(tokens)
