# Used modules
import random
import nltk
from pronouncing import rhymes

# The text from the gutenberg library that will be useD
CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')

def clean_corpus(corpus):
    filter_words = [';', ':']
    corpus_new = []
    for word in corpus:
        clean_word = word.lower()
        
        try:
            if clean_word[0 : 2] == '--':
                clean_word = clean_word[2 : len(clean_word)]
        except:
            pass
        try:
            if clean_word[-2 : len(clean_word)] == '--':
                clean_word = clean_word[0 : -2]
        except:
            pass
        
        if clean_word not in filter_words and len(clean_word) != 0:
            corpus_new.append(clean_word)
    
    return corpus_new

def generate_CFD(corpus):
    bigram = nltk.bigrams(CORPUS)
    return nltk.ConditionalFreqDist(bigram)

def generate_poem(num_words):
    poem = ''
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = random.choice(CORPUS_CLEAN) # potentially improve this so it's not an adjective or verb
    for i in range(num_words):
        if word in CFD: # this conditional can also be modified so the loop does not end early
            poem += (word + ' ')
            word = random.choice(list(CFD[word].keys()))
        else:
            break
    return poem

# Break cases:
# sometimes the entire poem is empty
# the parsing issue
# sometimes when the first word is weird the whole thing gets weird
