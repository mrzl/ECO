import gensim
# used for loading or saving
model_file = '/home/ramin/projects/ECO/src/python/modelbuilder/parsed_v3_valid.doc2vec'


# Build sentence list (each sentence needs at least 1 tag)
filename = '/home/marcel/drive/data/eco/NAIL_DATAFIELD_txt/parsed_v3/parsed_v3_valid.txt'

sentences = []
from random import shuffle

for uid, line in enumerate(open(filename)):
    ls = gensim.models.doc2vec.LabeledSentence(words=line.split(), tags=['SENT_%s' % uid])
    sentences.append(ls)
print(len(sentences),'sentences')


# Training the doc2vec model

# tutorial https://rare-technologies.com/doc2vec-tutorial/
# proposes shuffling or learning reate adjustment. we gonna do both
# in total 20 epochs
model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
print('building vocab') 
model.build_vocab(sentences)

base_alpha = model.alpha
base_min_alpha = model.min_alpha

for mepoch in range(2):
    model.alpha = base_alpha 
    model.min_alpha = base_min_alpha
    for epoch in range(10):
        print('epoch',mepoch * 10 + epoch)
        model.train(sentences)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    shuffle(sentences)

# saving the model    
model.save(model_file)


# Loading the model

# model_loaded = gensim.models.Doc2Vec.load(model_file)

# Test: printing sentence 9 and getting the most similar ones.

print ' '.join(sentences[9][0])
sims = model_loaded.docvecs.most_similar('SENT_9')
print 'similar sentence',len(sims)
print '\nSIMILAR SENTENCES\n'
for sim in sims:
    print nice_print(sim)


# Tiny helper
def nice_print(tagged_doc):
    return ' '.join(sentences[int(tagged_doc[0][5:])][0])
