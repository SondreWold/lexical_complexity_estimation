# Support script for generating a large JSON to be used in a front end application, not directly related to the research paper.
import codecs
from pathlib import Path
from statistics import median
from tqdm import tqdm
import argparse
import gensim
import ijson
import json
from utils import load_embedding


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=Path, help="Lemmatized file")
    parser.add_argument("--output_path", type=Path, help="Output file path")
    args = parser.parse_args()
    return args


def chunk_generator():
    for lemma in tqdm(lemmas):
        # Note: We do not have a PoS tagged Word2vec model, do we?
        og_lemma = lemma["lemma"]
        word = og_lemma.split("_")[0]
        score = lemma["cs"]
        if word not in model.key_to_index:
            continue
        synonyms = []

        for synonym, sim in model.most_similar(positive=[word], topn=5):
            if synonym in keys:
                synonyms.append({"lemma": synonym, "similarity": sim})

        if len(synonyms) > 0:
            entity = {word: {"complexity_score": score, "synonyms": synonyms}}
            yield entity


# https://stackoverflow.com/questions/36157634/how-to-incrementally-write-into-a-json-file
class StreamArray(list):
    """
    Converts a generator into a list object that can be json serialisable
    while still retaining the iterative nature of a generator.

    IE. It converts it to a list without having to exhaust the generator
    and keep it's contents in memory.
    """
    def __init__(self, generator):
        self.generator = generator
        self._len = 1

    def __iter__(self):
        self._len = 0
        for item in self.generator:
            yield item
            self._len += 1

    def __len__(self):
        """
        Json parser looks for a this method to confirm whether or not it can
        be parsed
        """
        return self._len


if __name__ == "__main__":
    args = parse_args()

    # Loading and global scoping the model and lemmas
    print("Loading Word2Vec model...")
    model = load_embedding("./models/model.bin")
    result = {}
    print("Loading lemma list...")
    with open(args.input_path, "r", encoding="utf-8") as f:
        lemmas = json.load(f)
    lemmas = lemmas["lemmas"]
    keys = [l["lemma"].split("_")[0] for l in lemmas]

    # Stream writing the json objects
    with open(args.output_path, "w", encoding="utf-8") as f:
        generator = chunk_generator()
        stream_array = StreamArray(generator)
        for chunk in json.JSONEncoder(ensure_ascii=False).iterencode(stream_array):
            f.write(chunk)
