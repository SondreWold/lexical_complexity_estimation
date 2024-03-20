import gensim
import numpy as np
from scipy import stats
import json


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
