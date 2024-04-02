import json
import argparse
from tqdm import tqdm


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        args (Namespace): The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the lemmatized corpus")
    parser.add_argument("-l", "--lix_input", type=str, required=True, help="Path to the lix overview")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output inverted index file")

    args = parser.parse_args()  
    return args


def save_inverted_index_json(index, path):
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(index, fp, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    args = parse_args()
    inverted_index = {}

    with open(args.input, "r") as f:
        corpus = json.load(f)
    
    with open(args.lix_input, "r") as f:
        lix_scores = json.load(f)
    
    print(f"Number of documents in corpus: {len(corpus)}")

    for document in tqdm(corpus):
        doc_lix_score = lix_scores[document["url"]]
        doc_index = {}
        for i in range(len(document["stanza"])):
            for lemma, pos in zip(document["stanza"][i]["lemma"], document["stanza"][i]["pos"]):
                if pos in ["PROPN", "NUM", "PUNCT", "X"]:
                    continue
                key = f"{lemma}_{pos}"
                if key in doc_index:
                    continue
                else:
                    doc_index[key] = doc_lix_score
            
        for key, value in doc_index.items():
            if key in inverted_index:
                inverted_index[key].append(value)
            else:
                inverted_index[key] = [value]
        
    print(f"Number of lemmas in inverted index: {len(inverted_index.keys())}")
    save_inverted_index_json(inverted_index, args.output)
