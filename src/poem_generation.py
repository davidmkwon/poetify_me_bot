# Used modules
import random
import nltk
from nltk.corpus import wordnet
from pronouncing import rhymes

CORPUS = open("6524-8.txt", "r", encoding="ISO-8859-1").read()
# CORPUS = ''.join([i for i in CORPUS if not i.isdigit()]).split(' ')
# CORPUS = ''.join([i for i in CORPUS if not i.isdigit()]).replace("\n\n", " "w
# CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')

def clean_corpus(corpus):
    #filter and trail words to cut out
    filter_words = [':',',','"', '-', "'", 's', '),' ,',--']
    trail_words = ['--', '"', '_', ']', '[', "'", '__']
    corpus_new = []
    
    #filer out line breaks
    corpus = corpus.replace('\n\n', ' ')
    corpus = corpus.replace('\n', ' ')
    corpus = corpus.split(' ')

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

        if clean_word not in filter_words and word and not clean_word.isdigit():
            corpus_new.append(clean_word)
    
    return corpus_new

def print_corpus():
    corpus_clean = clean_corpus(CORPUS)
    for word in corpus_clean:
        print(word),

def generate_CFD(corpus):
    bigram = nltk.bigrams(corpus)
    return nltk.ConditionalFreqDist(bigram)

def generate_raw_naive_poem(num_words):
    poem = ''
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = find_random_first_word(CORPUS_CLEAN)

    for i in range(num_words):
        if word in CFD:
            poem += (word + ' ')
            word = random.choice(list(CFD[word].keys()))
        else:
            break

    return poem

def find_random_first_word(corpus):
    valid_first_word_POS = ['NN', 'NNS', 'NNP', 'NNPS']
    word = random.choice(corpus)
    LIMIT = 100
    for i in range(LIMIT):
        POS_tag = nltk.pos_tag([word])
        if POS_tag[0][1] in valid_first_word_POS:
            break
        word = random.choice(corpus)
        if i == LIMIT - 1:
            raise Error('Cannot locate a valid word')
    
    return word

def generate_raw_poem(words_per_line = 10, height = 4):
    if height % 2 != 0:
        raise InputError('Height value must be even.')

    poem = [[] for i in range(height)]
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = find_random_first_word(CORPUS_CLEAN)
    
    invalid_end_word_POS = ['IN', 'WDT', 'DT', 'CC']
    sentence_count = words_per_line * height / 2 # assume default ABAB rhyme scheme
    current_word_count = 0
    row_num = 0
    
    for i in range(height // 2):
        while current_word_count < sentence_count:
            if word in CFD:
                poem[row_num].append(word)
                word = random.choice(list(CFD[word].keys()))
                current_word_count += 1
                
                if current_word_count == sentence_count // 2:
                    row_num += 1 
                
                if current_word_count == sentence_count:
                    if poem[row_num][-1] in invalid_end_word_POS:
                        
                        original_word = word
                        while poem[row_num][-1] not in invalid_end_word_POS:
                            for each_word in list(CFD[poem[row_num][-1]].keys()):
                                if each_word not in invalid_end_word_POS:
                                    word = each_word
                                    poem[row_num].append(word)
                                    break
                            
                            if word == original_word:
                                word = random.choice(list(CFD[poem[row_num][-1]].keys()))
                                poem[row_num].append(word)
                    
                    current_word_count = 0
                    row_num += 1
                    word = find_random_first_word(CORPUS_CLEAN)
                    break
            
            else:
                reverse_count = Math.log(sentence_count)
                current_word_count -= reverse_count # make sure this doesn't overlap into previous row
                word = poem[row_num][-reverse_count]

    return poem

# def rhyme_poem(poem):


'''
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
