# Used libaries
import random
import math
import nltk
from nltk.corpus import wordnet
import pronouncing

CORPUS = open("sbcorpus.txt", "r", encoding="ISO-8859-1").read()
FILTER_WORDS = [':',',','"', '-', "'", 's', '),' ,',--']
TRAIL_WORDS = ['--', '"', '_', ']', '[', "'", '__', ',']

def clean_corpus(corpus):
    '''
    This method takes in some body of text, and filters out of the corpus
    all filter words and trail words defined in this file. The method returns
    a list of the "cleaned" words from the parameter corpus
    '''

    corpus_new = []
    
    #filer out line breaks
    corpus = corpus.replace('\n\n', ' ')
    corpus = corpus.replace('\n', ' ')
    corpus = corpus.split(' ')

    for word in corpus:
        clean_word = word.lower()

        for trail_word in TRAIL_WORDS:
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

        if clean_word not in FILTER_WORDS and word and not clean_word.isdigit():
            corpus_new.append(clean_word)
    
    return corpus_new

def generate_CFD(corpus):
    '''
    This method creates and returns a Conditional Frequency Distribution
    using nltk's ConditionalFreqDist function. The CFD is generated using
    a constructed bigram of the parameter corpus
    '''

    bigram = nltk.bigrams(corpus)
    return nltk.ConditionalFreqDist(bigram)

def POS(word):
    '''
    This method returns the part of speech of a word, relying on nltk's
    pos_tag library.
    '''

    word_POS = nltk.pos_tag([word])
    return word_POS[0][1]

def find_random_first_word(corpus):
    '''
    This method returns a random word from the parameter corpus, given some
    conditions: first, the word must be "valid", meaning it's part of speech is
    one of those listed below; second, the word must be chosed within some limit.
    If the limit is exceeded, a word is chosen from random.
    '''

    LIMIT = 100
    valid_first_word_POS = ['NN', 'NNS', 'NNP', 'NNPS']
    word = random.choice(corpus)
    for i in range(LIMIT):
        if POS(word) in valid_first_word_POS:
            break
        word = random.choice(corpus)
        if i == LIMIT - 1:
            return random.choise(corpus)
    
    return word

def generate_raw_naive_poem(num_words):
    '''
    This method generates a random poem using a simple markov chaining method
    based off the CFD of a corpus. This method is not used anymore, rather was
    written for testing purposes.
    '''

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

def generate_raw_poem(words_per_line = 10, height = 4):
    '''
    This method generates a random, raw poem. This entails that the some randomly
    generated sequence of words (most likely two sentences) will be generated and
    returned as a 2D array (list of lists). This method uses a simple markov chaining
    method based off the CFD of a corpus. There are many steps the method takes to ensure
    that the generated poem will be valid.
    '''

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
    LIMIT = 10
    iteration = 0 # used for the limit counter
    row = 0

    while row < height // 2:
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
                        print('next iteration')

                        try:
                            last_word = poem[row][-1]
                        except:
                            last_word = find_random_first_word(CORPUS_CLEAN)

                        if CFD[last_word].keys():
                            word = random.choice(list(CFD[last_word].keys()))
                        else:
                            word = find_random_first_word(CORPUS_CLEAN)

                        current_word_count -= 1
                        iteration += 1
                        
                        if iteration == LIMIT:
                            # restart the entire function
                            current_word_count = 0
                            iteration = 0
                            poem = [[] for i in range(height//2)]
                            word = find_random_first_word(CORPUS_CLEAN)


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

        row += 1

    return poem

def rhyme_poem(poem):
    '''
    This method rhymes a poem. It takes a given poem (stored as a 2D array) and
    first checks if the poem is already rhyming. If not, then the method will first
    see if there are any synonyms of the 2nd last word that rhyme with the 1st last word.
    If none, then the process will repeat for vice versa. Lastly, if this does not work,
    the method will randomly pick a word that rhymes with the 1st last word.
    '''

    # initial check if poem is already rhyming
    end_word_1 = poem[0][-1]
    end_word_2 = poem[1][-1]
    end_words = [end_word_1, end_word_2]

    if end_word_1 in pronouncing.rhymes(end_word_2) or end_word_2 in pronouncing.rhymes(end_word_1):
        return poem

    for i in range(2): 

        synonyms = []
        for each_syn in wordnet.synsets(end_words[1 - i]): #end_words[1 - i]
            for lemma in each_syn.lemmas():
                synonyms.append(lemma.name())

        rhymes = pronouncing.rhymes(end_words[i]) #end_words[i]
        for rhyme in rhymes:
            if rhyme in synonyms:
                poem[1 - i][-1] = rhyme #poem[1 - i][-1]
                return poem

        pos_end_word = POS(end_words[1 - i]) #end_words[1 - i]

        for rhyme in rhymes:
            if POS(rhyme) == pos_end_word:
                poem[1 - i][-1] = rhyme #end_word[1 - i]
                return poem

    # none of the above tactics worked, just replace the 2nd end word with a random rhyming word, or vice versa
    for i in range(2):
        rhymes = pronouncing.rhymes(end_words[i])
        if rhymes:
            random_rhyme = random.choice(rhymes)
            poem[1 - i][-1] = random_rhyme

    return poem
