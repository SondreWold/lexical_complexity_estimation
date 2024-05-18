import gensim
import numpy as np
import json
import re
from scipy import stats

class Stavelse:
    def __init__(self):
        self.vowellist = "[aeiouyæøåéüèáàóò]+"
        self.diphthongs = ["au","øy","ei","oi","ai"]

    def stav(self,word):
        """Takes a word and outputs the number of syllables,
            based on the number and types of vowels.
            98.2% accuracy on the uttalekorpus.
            str: word - the word for which syllables is predicted
        """
        vowels = re.findall(self.vowellist, word.lower())
        newvowels = []
        for vow in vowels:
            if len(vow) == 1:
                newvowels.append(vow)
            else:
                vow_iter = iter(vow)
                first = next(vow_iter,"")
                while first != "":
                    second = next(vow_iter,"")
                    if first+ second in self.diphthongs:
                        newvowels.append(first+second)
                        first = next(vow_iter,"")
                    else:
                        newvowels.append(first)
                        first = second
        return newvowels


def print_kolmogorov(name, value1, value2):
    result = stats.ks_2samp(value1, value2, alternative="two-sided")
    output = {
        'statistic': result.statistic,
        'pvalue': result.pvalue,
    }
    with open(f"./outputs/{name}.json", "w") as outfile:
        json.dump(output, outfile)


def load_corpora(path, cutoff=100):
    with open(path, 'r') as f:
        data = json.load(f)
    data = [x for x in data.values() if x < cutoff]
    data = reject_outliers(np.array(data)).tolist()
    return data


def load_embedding(modelfile):
    # Detect the model format by its extension:
    # Binary word2vec format:
    if modelfile.endswith(".bin.gz") or modelfile.endswith(".bin"):
        emb_model = gensim.models.KeyedVectors.load_word2vec_format(
            modelfile, binary=True, unicode_errors="replace"
        )
    # Text word2vec format:
    elif (
            modelfile.endswith(".txt.gz")
            or modelfile.endswith(".txt")
            or modelfile.endswith(".vec.gz")
            or modelfile.endswith(".vec")
    ):
        emb_model = gensim.models.KeyedVectors.load_word2vec_format(
            modelfile, binary=False, unicode_errors="replace"
        )
    else:  # Native Gensim format?
        emb_model = gensim.models.KeyedVectors.load(modelfile)
        #  If you intend to train the model further:
        # emb_model = gensim.models.Word2Vec.load(embeddings_file)
    return emb_model


def reject_outliers(data, m=4):
    return data[abs(data - np.mean(data)) < m * np.std(data)]
