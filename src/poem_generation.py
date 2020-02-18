# Used modules
import random
import nltk
from nltk.corpus import wordnet
from pronouncing import rhymes

# The text from the gutenberg library that will be useD
CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')

def clean_corpus(corpus):
    filter_words = [':',',','"', '-', "'", 'austen', 'jane', '1816', 'ii', 's']
    trail_words = ['--', '"', '_', ']', '[', "'"]
    corpus_new = []
    for word in corpus:
        clean_word = word.lower()

        for trail_word in trail_words:
            size = len(trail_word)
            try:
                if clean_word[0 : size] == trail_word:
                    clean_word = clean_word[size : len(clean_word)]
            except: pass
            try:
                if clean_word[-size : len(clean_word)] == trail_word:
                    clean_word = clean_word[0 : -size]
            except: pass

        if clean_word == ';':
            clean_word = '.'
        
        if clean_word not in filter_words and len(clean_word) != 0:
            corpus_new.append(clean_word)
    return corpus_new

def generate_CFD(corpus):
    bigram = nltk.bigrams(corpus)
    return nltk.ConditionalFreqDist(bigram)

def generate_raw_naive_poem(num_words):
    poem = ''
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = random.choice(CORPUS_CLEAN)

    validFirstWordPOS = ['NN', 'NNS', 'NNP', 'NNPS']
    while True:
        POS_tag = nltk.pos_tag([word])
        if POS_tag[0][1] in validFirstWordPOS:
            break
        word = random.choice(CORPUS_CLEAN)

    for i in range(num_words):
        if word in CFD: # this conditional can also be modified so the loop does not end early
            poem += (word + ' ')
            word = random.choice(list(CFD[word].keys()))
        else:
            break

    return poem

def generate_raw_poem(words_per_line, height):
    poem = [['' for i in range(words_per_line)] for j in range(height)]
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = random.choice(CORPUS_CLEAN) # potentially improve this so it's not an adjective or verb
    
    return poem
    '''
    for j in range(height):
        for i in range(words_per_line):
            poem[j][i] = word
            if len(list(CFD[word].keys())) > 1:
                original_word = word
                while True:
                    word = random.choice(list(CFD[original_word].keys()))
                    if word in CFD:
                        break
            elif len(CFD[word].keys() == 1:
                word = list(CFD[word].keys())[0]
    '''

# def rhyme_poem(poem):


'''
Break cases:
somtimes the entire poem is empty

Steps for forward-bigram construction
1. generate forward bigram of entire gutenberg text
2. create ConditionalFreqDist
3. let's say poem is 4 lines --> generate 20-28 words
4. rhyme (ABAB scheme):
    a) first check if the poem is already in ABAB scheme (it probably isn't)
    b) if not, find all rhymes of the first last word
    c) check if any of these rhymes are synonyms of the third last word --> we want to
    maintain original meaning as much as possible
    d) if there are none, then pick a synonym that has the same POS (part of speech)
    as the third last word
    e) repeat for lines 2 and 4
5. make first word be a synonym of the user inputted word
'''
