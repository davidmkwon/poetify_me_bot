# Used modules
import random
import math
import nltk
from nltk.corpus import wordnet
from pronouncing import rhymes

CORPUS = open("6524-8.txt", "r", encoding="ISO-8859-1").read()
# CORPUS = nltk.corpus.gutenberg.words('austen-emma.txt')

def clean_corpus(corpus):
    #filter and trail words to cut out
    filter_words = [':',',','"', '-', "'", 's', '),' ,',--']
    trail_words = ['--', '"', '_', ']', '[', "'", '__', ',']
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

def POS(word):
    word_POS = nltk.pos_tag([word])
    return word_POS[0][1]

def find_random_first_word(corpus):
    valid_first_word_POS = ['NN', 'NNS', 'NNP', 'NNPS']
    word = random.choice(corpus)
    LIMIT = 100
    for i in range(LIMIT):
        if POS(word) in valid_first_word_POS:
            break
        word = random.choice(corpus)
        if i == LIMIT - 1:
            raise Error('Cannot locate a valid word')
    
    return word

def generate_raw_poem(words_per_line = 10, height = 4):
    if height % 2 != 0:
        raise InputError('Height value must be even.')

    poem = [[] for i in range(height // 2)]
    CORPUS_CLEAN = clean_corpus(CORPUS)
    CFD = generate_CFD(CORPUS_CLEAN)
    word = find_random_first_word(CORPUS_CLEAN)
    
    invalid_end_word_POS = ['IN', 'WDT', 'DT', 'CC', 'JJ', 'PRP$']

    # assume use of default ABAB rhyme scheme
    sentence_count = words_per_line
    current_word_count = 0

    for row in range(height//2):
        while current_word_count < sentence_count:
            if word in CFD:
                poem[row].append(word)
                word = random.choice(list(CFD[word].keys()))
                current_word_count += 1

                # case where the word added has a period ending
                if poem[row][-1][-1] == '.':
                    # if this ending is too quick, then randomly pick another word to continue with
                    if current_word_count < sentence_count - int(math.log(sentence_count)):
                        poem[row].pop()
                        print(len(poem[row]))

                        try:
                            last_word = poem[row][-1]
                        except:
                            last_word = find_random_first_word(CORPUS_CLEAN)

                        word = random.choice(list(CFD[last_word].keys()))
                        current_word_count -= 1
                    # if this ending is not too quick, then exit this loop and begin the next sentence
                    else:
                        current_word_count = 0
                        word = find_random_first_word(CORPUS_CLEAN)
                        break

                if current_word_count == sentence_count:
                    print('The end word right now is ', poem[row][-1])

                    if POS(poem[row][-1]) in invalid_end_word_POS:
                        print('there is an invalid ending right now')
                        
                        while POS(poem[row][-1]) in invalid_end_word_POS:
                            original_word = word
                            for each_word in list(CFD[poem[row][-1]].keys()):
                                if POS(each_word) not in invalid_end_word_POS:
                                    word = each_word
                                    poem[row].append(word)
                                    print('I have found the valid word ', each_word)
                                    break

                            if word == original_word:
                                word = random.choice(list(CFD[word].keys()))
                                poem[row].append(word)

                    current_word_count = 0
                    word = find_random_first_word(CORPUS_CLEAN)
                    break

            else:
                reverse_count = int(math.log(sentence_count))
                current_word_count -= reverse_count
                for i in range(reverse_count):
                    poem.pop()
                word = poem[row][-1]

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
