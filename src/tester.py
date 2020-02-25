import poem_generation
import poem_generation2
import pronouncing
import random
import nltk

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

poem_rhyme = poem_generation.generate_raw_poem()
for line in poem_rhyme:
    string = ''
    for word in line:
        word_POS = nltk.pos_tag([word])
        word_POS = word_POS[0][1]
        string += (word + ' ' + '(' + word_POS + ')')
    print (string)
