import poem_generation
import pronouncing
import random
import nltk

for i in range(5):
    poem_clean = poem_generation.generate_raw_naive_poem(20)
    print(poem_clean)

print('\nNON-NAIVE POEMS BELOW\n')

for i in range(5):
    poem_rhyme = poem_generation.generate_raw_poem()
    for line in poem_rhyme:
        string = ''
        for word in line:
            string += (word + ' ')
        print (string)
    print('\nNEXT POEM\n')
