"""Neste script usaremos duas bibliotecas.
O spacy para anotação e o re para as expressões regulares.
Para importar uma biblioteca, usamos:
"""
# %%
import spacy
import re
# %% """E então carregamos o modelo para anotação de textos em português"""

nlp = spacy.load('en_core_web_sm')
# para textos em inglês, podemos utilizar o modelo abaixo
#nlp = spacy.load('en_core_web_sm')

#%%

text = "Eloise and John are having a child. They are pretty happy about it. Martha, and Julia, on the other side, don't seem to like the idea very much. It is still a surprise for them. Eloise, Lisa and Julia bought a gift to Marie, Alex, Oscar and John. They really loved the gift. For what hell Regina Soares stand for. They."
#%%"""removemos as quebras de linha (\n)"""

text = re.sub(r'\n', '', text)

# %%"""fazemos a anotação"""

nlp_text = nlp(text)
nlp_text
# %%"""convertemos o resultado para o formato vertical"""

def print_nlp(nlp):
    tagged_text = ""
    for token in nlp:
        tagged_text += "{}\t{}\t{}\t{}\t{}\t{}\n".format(str(token.text), str(token.lemma_), str(token.tag_), str(token.pos_), str(token.head.text), str(token.dep_))

    print(tagged_text)

def find_prons(nlp):
    return list(filter(
        lambda tk: tk[1].pos_ == "PRON" and tk[1].lemma_ == "they",
        enumerate(nlp)
        )
    )

nlp_pron = find_prons(nlp_text)

def find_puncts(nlp):
    return list(filter(
        lambda tk: tk[1].pos_ == "PUNCT" and tk[1].tag_ == ".",
        enumerate(nlp)
        )
    )

nlp_punct = find_puncts(nlp_text)
print(nlp_pron, nlp_punct)
print_nlp(nlp_text[30:60])
#%%

def get_last_phrase(i, nlp_punct):
    if i == 0:
        return nlp_text[
            0:nlp_punct[i][0]+1
        ]
    return nlp_text[
        nlp_punct[i-1][0]+1:nlp_punct[i][0]+1
    ]

def get_last_punct_idx(i, nlp_punct):
    return list(filter(
        lambda t: t[1][0] < i,
        enumerate(nlp_punct)
    ))[-1][0]

def get_nouns_from_phrase(phrase):
    return set(filter(
            lambda term: len(re.findall(r"NN\w*", term[1].tag_)) > 0,
            enumerate(phrase)
        ))

def get_capital_words(phrase):
    words = list(filter(
            lambda term: term[1].text[0].isupper(),
            enumerate(phrase)
        ))
    
    filtered_words = list()

    i = 0
    while i < len(words):
        j = 1
        root_idx = words[i][0]
        next_idx = words[i+j][0]
        filtered_words.append(words[i])
        if root_idx+j == next_idx:
            while True:
                print("i,j",i,j)
                j += 1
                next_idx = words[i+j][0]
                if root_idx+j != next_idx:
                    i += j
                    print("BREAK")
                    break
                print("root_idx+j",root_idx+j)
                print("next_idx", next_idx)
        i += 1
    
    return filtered_words
                
def get_capital_words_rev(phrase):
    words = list(filter(
            lambda term: term[1].text[0].isupper(),
            enumerate(phrase)
        ))
    
    filtered_words = list()

    i = len(words)-1
    while i >= 0:
        #j=-1
        #flag=1
        if i == 0:
            filtered_words.append(words[i])
            #i -= 1
            break
        if(words[i-1][0] == (words[i][0]-1)):
            i -= 1
        else:
            filtered_words.append(words[i])
            i -= 1
            #do {
            #    words[i-1]
            #    j -= 1
            #    if(v[i-j].index==(v[i].index-j)):
            #        deleta v[i-1]
            #    else:
            #        flag=0
            #} while(flag!=0)
        #i -= 1
    filtered_words.reverse()
    return filtered_words




def get_words_dependence(phrase):
    return set(filter(
            lambda term: term[1].dep_ in ["nsubj", "conj"],
            enumerate(phrase)
        ))

def get_last_phrase_recursive(pron, puncts):
    if len(puncts) == 0:
        return ""

    last_punct_idx = get_last_punct_idx(pron[0], puncts)
    phrase = get_last_phrase(last_punct_idx, puncts)

    capital_words = get_capital_words_rev(phrase)
    nouns = get_nouns_from_phrase(phrase)
    dep_words = get_words_dependence(phrase)

    words = capital_words
    
    for word in words:
        score = 1
        if word in nouns:
            score += 1
        if word in dep_words:
            score += 1
        
    print(words, score)
    if len(words) >= 2:
        return phrase
    else:
        return get_last_phrase_recursive(pron, puncts[:-1])

def map_prons_to_last_phrase(prons, puncts):
    pron_dict = {}
    for pron in prons:
        pron_dict[pron] = get_last_phrase_recursive(pron, puncts)
            
    return pron_dict

prons_to_phrase = map_prons_to_last_phrase(nlp_pron, nlp_punct)
prons_to_phrase
#%%


def map_prons_to_nouns(prons, puncts):
    pron_dict = {}
    prouns_phrases = map_prons_to_last_phrase(prons, puncts)
    for pron in prons:
        pron_dict[pron] = get_nouns_from_phrase(prouns_phrases[pron])
    return pron_dict


mapped = map_prons_to_nouns(nlp_pron, nlp_punct)
for pronoun, nouns in mapped.items():
    print([(noun[0] - pronoun[0], noun[1]) for noun in nouns])
        

#%%
list(
    map(
        lambda punct:
            list(filter(           
                lambda pron: pron[1] < punct[1],
                nlp_pron
            ))
    ,nlp_punct)
)

#print_nlp(nlp_text[40:65])


# %%
