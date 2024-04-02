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
from utils import load_embedding, reject_outliers, Stavelse


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

def plot_average(lemma_list):
    complexity_scores = [get_complexity_score(word) for word, value in lemma_list.items()]
    plt.figure(figsize=(14,7))
    plt.hist(complexity_scores, alpha=.9, bins='auto')
    plt.xlabel("Complexity score", fontsize=20)
    plt.ylabel("Count", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.grid(False)
    plt.savefig("./outputs/averages.pdf", format="pdf", bbox_inches="tight")
    plt.close()

def low_freq(lemma_list, marker):
    lengths_raw = [len(value) for key, value in lemma_list.items() if len(value) < marker]
    complexity_scores_raw = [median(value) for key, value in lemma_list.items() if len(value) < marker]
    complexity_scores = [get_complexity_score(word) for word, value in lemma_list.items() if len(value) < marker]
    idx = [random.randint(1, 10000) for _ in range(0,10000)]
    complexity_scores = np.array(complexity_scores)[idx]
    complexity_scores_raw = np.array(complexity_scores_raw)[idx]
    lengths_raw = np.array(lengths_raw)[idx]
    plt.scatter(complexity_scores_raw, lengths_raw, label="Raw")
    plt.scatter(complexity_scores, lengths_raw, alpha=0.2, label="Normalized")
    plt.xlabel("Complexity", fontsize=20)
    plt.ylabel("Frequency", fontsize=20)
    plt.xticks(fontsize=20)
    plt.legend()
    plt.legend(prop={'size': 12})
    plt.savefig("./outputs/corr_low_freq.pdf", format="pdf", bbox_inches="tight")
    plt.close()

def high_freq(lemma_list, marker):
    lengths_raw = [len(value) for key, value in lemma_list.items() if len(value) > marker]
    complexity_scores_raw = [median(value) for key, value in lemma_list.items() if len(value) > marker]
    complexity_scores = [get_complexity_score(word) for word, value in lemma_list.items() if len(value) > marker]
    plt.scatter(complexity_scores_raw, lengths_raw, label="Raw")
    plt.scatter(complexity_scores, lengths_raw, alpha=0.2, label="Normalized")
    plt.axvline(x = median(complexity_scores_raw), color = 'b', label = 'Median raw complexity score')
    plt.xlabel("Complexity", fontsize=20)
    plt.ylabel("Frequency", fontsize=20)
    plt.xticks(fontsize=20)
    plt.legend()
    plt.legend(prop={'size': 12})
    plt.savefig("./outputs/corr_high_freq.pdf", format="pdf", bbox_inches="tight")
    plt.close()


def word_length(lemma_list):
    wl_len = [len(key.split("_")[0]) for key, value in lemma_list.items()]
    cs_len = [get_complexity_score(word) for word, value in lemma_list.items()]
    idx = [random.randint(1, 10000) for _ in range(0,10000)]
    wl_len = np.array(wl_len)[idx]
    cs_len = np.array(cs_len)[idx]
    plt.scatter(cs_len, wl_len, label="Lemma")
    plt.axhline(y = median(wl_len), color = 'b', label = 'Median word length')
    plt.xlabel("Complexity", fontsize=20)
    plt.ylabel("Word length", fontsize=20)
    plt.xticks(fontsize=20)
    plt.legend()
    plt.legend(prop={'size': 12})
    plt.savefig("./outputs/word_lengths.pdf", format="pdf", bbox_inches="tight")
    plt.close()


def syllabbles(lemma_list):
    staver = Stavelse()
    syl = [len(staver.stav(word.split("_")[0])) for word, value in lemma_list.items()]
    cs_syl = [get_complexity_score(word) for word, value in lemma_list.items()]
    idx = [random.randint(1, 10000) for _ in range(0,10000)]
    cs_syl = np.array(cs_syl)[idx]
    syl = np.array(syl)[idx]
    plt.scatter(cs_syl, syl, label="Lemma")
    plt.axhline(y = median(syl), color = 'b', label = 'Median syllables')
    plt.xlabel("Complexity", fontsize=20)
    plt.ylabel("Syllables", fontsize=20)
    plt.xticks(fontsize=20)
    plt.legend()
    plt.legend(prop={'size': 12})
    plt.savefig("./outputs/syllables.pdf", format="pdf", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    n_doc = 135025
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

    plot_average(lemma_list)
    low_freq(lemma_list, marker=0.05*n_doc)
    high_freq(lemma_list, marker=0.05*n_doc)
    word_length(lemma_list)
    syllabbles(lemma_list)

