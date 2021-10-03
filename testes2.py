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

text = "Eloise and John are having a child. They are pretty happy about it. Eloise and Julia, on the other side, don't seem to like the idea very much. It is still a surprise for them. Eloise, Lisa and Julia bought a gift to Marie, Alex, Oscar and John. They really loved the gift. For what hell Regina Soares stand for."
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

def filter_by_nome_composto(words):
    filtered_words = list()

    i = len(words)-1
    while i >= 0:
        if i == 0:
            filtered_words.append(words[i])
            break
        if(words[i-1][0] == (words[i][0]-1)):
            i -= 1
        else:
            filtered_words.append(words[i])
            i -= 1
    filtered_words.reverse()
    return filtered_words

def get_capital_words_rev(phrase):
    words = list(filter(
            lambda term: term[1].text[0].isupper(),
            enumerate(phrase)
        ))

    words = filter_by_nome_composto(words)

    grouped_words = list()

    i = len(words)-1
    while i >= 0:
        group = list()
        while True:
            #print(i)
            #print(phrase[words[i][0]])
            #print(phrase[words[i][0]-1].text)
            if phrase[words[i][0]-1].text=='and':
                if phrase[words[i][0]-2].text[0].isupper():
                    #print("Append AND ISUPPER")
                    group.append(words[i])
                    i -= 1
                    continue
            elif phrase[words[i][0]-1].text==',':
                if phrase[words[i][0]-2].text[0].isupper():
                    #print("Append , ISUPPER")
                    group.append(words[i])
                    i -= 1
                    continue
            else:
                #print("APPEND AND BREAK")
                group.append(words[i])
                i-=1
                break
            if i < 0:
                break
        if len(group) > 1:
            grouped_words.append(group)
    
    return grouped_words

def get_words_dependence(phrase):
    return set(filter(
            lambda term: term[1].dep_ in ["nsubj", "conj"],
            enumerate(phrase)
        ))

def get_last_phrase_recursive(pron, puncts):
    if len(puncts) == 0:
        return ""

    # last end of sentence before the specific pronoun
    last_punct_idx = get_last_punct_idx(pron[0], puncts)

    # last phrase before the end of sentence
    phrase = get_last_phrase(last_punct_idx, puncts)

    # words with first letter capitalized
    capital_words = get_capital_words_rev(phrase)

    # words with tag NN*
    nouns = get_nouns_from_phrase(phrase)

    # words with dependence as "nsubj" or "conj"
    dep_words = get_words_dependence(phrase)

    #first_word_not_noun = False
    #if capital_words[0][0] == 0 and (capital_words[0] not in #nouns or capital_words[0] not in dep_words):
    #    #print(capital_words)
    #    first_word_not_noun = False

    words = capital_words
    
    # for word in words:
    #     score = 1
    #     if word in nouns:
    #         score += 1
    #     if word in dep_words:
    #         score += 1
        
    #print(words, score)
    if len(words) >= 1:
        return phrase, words
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
import numpy as np

def proximity_penallity(groups):
    max_val = max(get_idx_val(groups))    
    mean_distance = np.array(
        [
            sum(
                [
                    noun[0]/max_val for noun in group
                ])/len(group) 
                for group in groups
        ]
    )
    return 1 - mean_distance

def apply_metrics(prons_to_phrase):
    new_dict = {}
    for pronoun, vals in prons_to_phrase.items():
        groups = vals[1]
        new_dict[pronoun] = (groups, get_metrics(groups))
    return new_dict 

def get_metrics(groups):
    metrics = np.array([1. for _ in groups])

    if len(groups) > 1:
        metrics -= proximity_penallity(groups)*0.8

    tag_p = list()
    for group in groups:
        tag_p.append(tag_penallity(group))

    metrics -= np.array(tag_p)*0.2

    return metrics

def tag_penallity(group):
    score = 0.
    for noun in group:
        is_noun = len(re.findall(r"NN\w*", noun[1].tag_)) > 0
        has_dependence_ok = noun[1].dep_ in ["nsubj", "conj"]
        if is_noun:
            score += .5
        if has_dependence_ok:
            score += .5
    return (1 - score/len(group))


def get_idx_val(groups):
    return np.array(
        [noun[0] for group in groups for noun in group]
    )

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
