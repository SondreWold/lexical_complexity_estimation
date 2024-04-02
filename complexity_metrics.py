from analysis.utils import Stavelse
import argparse
import json


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        args (Namespace): The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to input json file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output json file")
    args = parser.parse_args()
    return args


class Complexity:
    def __init__(self):
        self.stavelse = Stavelse()
        self.puncts = ['.', ',', '!', '?', '(', ')', '-', '[', ']', '"', '`', "'"]

    def textify(self, text):
        """Returns a text version of a document"""
        new = []
        for sent in text:
            new.append(" ".join(sent["tokens"]))
        return " ".join(new)

    def _remove_punct(self, token_list):
        punctlist = ['.', ',', '!', '?', '(', ')', '-', '[', ']', '"', '`', "'"]
        new = [token for token in token_list if token not in punctlist]
        return new

    def coleman_liau(self, text, info=False):
        characters = 0
        words = 0
        sentences = 0
        for sent in text:
            sentences += 1
            for word in sent["tokens"]:
                words += 1
                for letter in word:
                    characters += 1
        L = (characters / words) * 100
        S = (sentences / words) * 100
        if info:
            print("Chars: {} Words: {} Sentences: {}".format(characters, words, sentences))
        return 0.0588 * L - 0.296 * S - 15.8

    def lix(self, text, info=False):
        words = 0
        words6 = 0
        sentences = 0
        for sent in text:
            sentences += 1
            for word in sent["tokens"]:
                if word not in self.puncts:  # remove punctuation
                    words += 1
                    if len(word) > 6:
                        words6 += 1
        indeks = words/sentences + (100*(words6/words))
        if info:
            print("Setninger: {}\nOrd: {}\nOrd6: {}".format(sentences, words, words6))
        return indeks

    def nb_lix(self, text, info=False):
        """Lix, men der setningsantallet estimeres utifra antall setningsavsluttende tegn"""
        words = 0
        sentsplits = ['.', ':', '?', '!']
        words6 = 0
        sentences = 0
        for sent in text:
            for word in sent["tokens"]:
                if word in sentsplits:
                    sentences += 1
                if word not in self.puncts:
                    words += 1
                    if len(word) > 6:
                        words6 += 1
        indeks = words/sentences + (100*(words6/words))
        if info:
            print("Setninger: {}\nOrd: {}\nOrd6: {}".format(sentences, words, words6))
        return indeks


if __name__ == "__main__":
    args = parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    complexity = Complexity()
    results = {}
    for x in data:
        results[x["url"]] = complexity.lix(x["stanza"])

    print(f"Done calculating LIX for {len(results.keys())} documents... Saving to path: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
