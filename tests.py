#%%
import nltk
nltk.download('treebank')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')

#%%
sentence = "Marie and John are having a child. They are pretty happy about it. Heloise and Julia, on the other side, don't seem to like the idea very much. It is still a surprise for them. Still, Heloise and Julia bought a gift to Marie and John. They really loved the gift. For what hell they stand for"

translation = "Marie e John vão ter um filho. Eles estão muito felizes com isso. Heloísa e Julia, por outro lado, não parecem gostar muito da ideia. Ainda é uma surpresa para eles. Mesmo assim, Heloise e Julia compraram um presente para Marie e John. Eles realmente amaram o presente. Por que diabos eles representam"

tokens = nltk.word_tokenize(sentence)
tokens_trans = nltk.word_tokenize(translation)

#%%
tagged = nltk.pos_tag(tokens)

tagged_nouns = list(
    filter(
        lambda tup: (tup[0][1] in ["NNPS", "NNS", "NNP"] and tup[0][0][0].isupper()),
        map(
            lambda t: [t[1], t[0]], 
            enumerate(tagged)
        )
    )
)

tagged_pronouns = list(
    filter(
        lambda tup: tup[0][1] in ["PRP", "PRP$"],
        map(
            lambda t: [t[1], t[0]], 
            enumerate(tagged)
        )
    )
)

tagged_terminators = list(
    filter(
        lambda tup: tup[0][1] in ["."],
        map(
            lambda t: [t[1], t[0]], 
            enumerate(tagged)
        )
    )
)


#%%
from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

#%%
nltk.help.upenn_tagset()

#%%
from nltk.translate import AlignedSent, Alignment

algnsent = AlignedSent(tokens, , Alignment.fromstring('0-3 1-2 2-0 3-1'))
print(algnsent.words)
print(algnsent.mots)
print(algnsent.alignment)
#%%
import goslate
gs = goslate.Goslate()
print(gs.translate(sentence, 'pt'))