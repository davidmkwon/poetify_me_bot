# Used libraries
from poem_generation import *
import pronouncing
import random
from nltk.corpus import wordnet as wn

'''
for i in range(5):
    poem_clean = poem_generation.generate_raw_naive_poem(20)
    print(poem_clean)
'''

# print('\nNON-NAIVE POEMS BELOW\n')

'''
for i in range(5):
    poem_rhyme = poem_generation.generate_raw_poem(5, 4)
    for line in poem_rhyme:
        string = ''
        for word in line:
            string += (word + ' ')
        print (string)
    print('\nNEXT POEM\n')
'''

poem_rhyme = rhyme_poem(generate_raw_poem())

for line in poem_rhyme:
    print('\n NEW LINE \n')
    for word in line:
        print(word)

'''
for line in poem_rhyme:
    string = ''
    for word in line:
        word_POS = nltk.pos_tag([word])
        word_POS = word_POS[0][1]
        string += (word + ' ' + '(' + word_POS + ')')
    print (string)
'''
