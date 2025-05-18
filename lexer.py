import re

def simple_tokenize(sentence):
    """
    Splits a sentence into tokens (words and punctuation).
    """
    return re.findall(r"\w+|[^\w\s]", sentence, re.UNICODE)

def basic_pos_tagger(tokens):
    """
    Assigns POS tags to tokens using an expanded dictionary.
    """
    pos_dict = {
        # Determiners
        'a': 'DET', 'an': 'DET', 'the': 'DET', 'this': 'DET', 'that': 'DET', 'these': 'DET', 'those': 'DET',

        # Nouns (add plural and common words)
        'man': 'NOUN', 'woman': 'NOUN', 'dog': 'NOUN', 'dogs': 'NOUN', 'cat': 'NOUN', 'cats': 'NOUN',
        'boy': 'NOUN', 'girl': 'NOUN', 'apple': 'NOUN', 'house': 'NOUN', 'tree': 'NOUN', 'city': 'NOUN',
        'school': 'NOUN', 'car': 'NOUN', 'students': 'NOUN', 'teacher': 'NOUN', 'market':'NOUN', 'ram':'NOUN', 'home':'NOUN', 'compiler':'NOUN', 'project':'NOUN', 'birthday':'NOUN',

        # Verbs (base and conjugated)
        'run': 'VERB', 'runs': 'VERB', 'walk': 'VERB', 'walks': 'VERB', 'eat': 'VERB', 'eats': 'VERB',
        'bark': 'VERB', 'barks': 'VERB', 'chase': 'VERB', 'chases': 'VERB', 'see': 'VERB', 'sees': 'VERB',
        'like': 'VERB', 'likes': 'VERB', 'jump': 'VERB', 'jumps': 'VERB', 'going':'VERB', 'eating':'VERB', 'design':'VERB',

        # Auxiliary verbs
        'is': 'AUX', 'are': 'AUX', 'was': 'AUX', 'were': 'AUX', 'am': 'AUX', 'be': 'AUX', 'been': 'AUX',

        # Modal verbs
        'can': 'MODAL', 'could': 'MODAL', 'shall': 'MODAL', 'should': 'MODAL',
        'will': 'MODAL', 'would': 'MODAL', 'may': 'MODAL', 'might': 'MODAL', 'must': 'MODAL',

        # Pronouns
        'he': 'PRON', 'she': 'PRON', 'it': 'PRON', 'they': 'PRON', 'i': 'PRON', 'you': 'PRON',
        'we': 'PRON', 'me': 'PRON', 'him': 'PRON', 'her': 'PRON', 'us': 'PRON', 'them': 'PRON', 'my':'PRON',

        # Adjectives
        'big': 'ADJ', 'small': 'ADJ', 'red': 'ADJ', 'blue': 'ADJ', 'quick': 'ADJ', 'lazy': 'ADJ',

        # Adverbs
        'quickly': 'ADV', 'slowly': 'ADV', 'very': 'ADV', 'silently': 'ADV', 'well': 'ADV', 'today':'ADV',

        # Prepositions
        'in': 'PREP', 'on': 'PREP', 'under': 'PREP', 'above': 'PREP', 'beside': 'PREP', 'with': 'PREP', 'to':'PREP',

        # Conjunctions
        'and': 'CONJ', 'or': 'CONJ', 'but': 'CONJ', 'because': 'CONJ',

        # Interjections
        'wow': 'INTJ', 'hey': 'INTJ', 'oh': 'INTJ', 'ouch': 'INTJ',

        # Numerals
        'one': 'NUM', 'two': 'NUM', 'three': 'NUM', 'ten': 'NUM',

        # Punctuation
        '.': 'PUNCT', ',': 'PUNCT', '!': 'PUNCT', '?': 'PUNCT'
    }

    return [(token, pos_dict.get(token.lower(), 'UNK')) for token in tokens]



def lexical_analysis(sentence):
    """
    Tokenizes and tags a sentence.
    """
    tokens = simple_tokenize(sentence)
    return basic_pos_tagger(tokens)