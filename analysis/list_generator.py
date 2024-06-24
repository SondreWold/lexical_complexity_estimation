from pathlib import Path
from statistics import median
from tqdm import tqdm
import argparse
import gensim
import ijson
import json


cs = lambda x: median(x) * (1 - (len(scores)/135025))  # 135025 is the total number of documents from the collected corpora

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=Path, help="Lemmatized file")
    parser.add_argument("--output_path", type=Path, help="Output file path")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    print("Loading lemma list...")
    args = parse_args()
    result = {
            "lemmas": []
            }
    

    with open(args.input_path, "r", encoding="utf8") as f:
        lemma_list = json.load(f)
        lemma_list = {k: v for k, v in sorted(lemma_list.items(), key=lambda item: len(item[1]), reverse=True)}
        top_k = 40000
        for key, scores in tqdm(lemma_list.items()):
            pos = key.split("_")[1]
            if pos not in ["ADJ", "NOUN", "VERB", "ADV"]:
                continue
            if len(scores) > 0:
                complexity = cs(scores)
                result["lemmas"].append({"lemma": key, "cs": complexity})
                top_k -= 1
            if top_k < 1:
                break

    with open(args.output_path, "w", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False)

        
        
        
