import numpy as np
import matplotlib.pyplot as plt
import json
import random
from scipy.stats import norm
from scipy import stats
from scipy.optimize import curve_fit
import scipy as sp
from statistics import stdev, variance, mean, median
import gensim
import pandas as pd
from os import path
from scipy.stats.stats import pearsonr, spearmanr
from utils import load_embedding, reject_outliers


def get_complexity_score(word, m=135025):
    scores = lemma_list.get(word, -1)
    try:
        y = len(scores)
    except:
        y = 1
    if scores == -1:
        return -1
    s = median(scores) * (1 - (y/135025))  # m is the total number of documents.
    return s


def find_alternatives(word, model):
    og_word = word
    a = word.split("_")
    word, pos = a[0], a[-1]
    l = {word: {'Synonymity': 1, 'Complexity': get_complexity_score(og_word)}}
    for i in model.most_similar(positive=[word], topn=10):
        comp_score = get_complexity_score(i[0] + f'_{pos}')
        if comp_score == -1:
            continue
        l[i[0]] = {'Synonymity': i[1], 'Complexity': comp_score}
    try:
        print(pd.DataFrame.from_dict(l).T.sort_values(by=['Complexity'], ascending=True))
    except:
        print('Not able to produce alternatives!')


if __name__ == '__main__':
    with open("../../text_complexity/data/lemma_list_final.json", "r") as f:
        lemma_list = json.load(f)

    # Model can be downloaded from http://vectors.nlpl.eu/repository/
    embeddings_file = path.join("../../text_complexity/models/76/", "model.bin")
    model = load_embedding(embeddings_file)

    print(f"Number of lemmas before filtering: {len(lemma_list.keys())}")
    keys = []
    for key, value in lemma_list.items():
        lemma_list[key] = [x for x in lemma_list[key] if x < 100 or x > 10]
        if len(value) < 20 or key[0] == '_' or key.split("_")[-1] not in ["VERB", "NOUN", "ADJ", "ADV"]:
            keys.append(key)
        
    for key in keys:
        del lemma_list[key]
    print(f"Number of lemmas after filtering: {len(lemma_list.keys())}")

    find_alternatives('medføre_VERB', model=model)
    find_alternatives('ubehag_NOUN', model=model)
    find_alternatives('betrakte_VERB', model=model)
    find_alternatives('bestemt_ADJ', model=model)
    find_alternatives('undulat_NOUN', model=model)
    find_alternatives('fugl_NOUN', model=model)
