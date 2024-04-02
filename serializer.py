import argparse
import json
import stanza
from tqdm import tqdm
import pathlib


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        args (Namespace): The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=pathlib.Path, required=True,
                        help="Path to input json file")
    parser.add_argument("-o", "--output", type=pathlib.Path, required=True,
                        help="Path to output json file")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    with open(args.input, 'r') as f:
        data = json.load(f)
    
    urls = data['urls']
    documents = data['documents']
    nlp = stanza.Pipeline(lang='nb', processors='tokenize,pos,lemma')
    parsed_documents = []

    for i, (url, document) in tqdm(enumerate(zip(urls, documents))):
        document = document.replace('\n', '')
        doc = nlp(document)
        if len(doc.sentences) < 5:
            continue
        
        stanza_objects = []
        for sentence in doc.sentences:
            stanza_object = {
                'tokens': [word.text for word in sentence.words if len(sentence.words) > 1],
                'lemma': [word.lemma for word in sentence.words if len(sentence.words) > 1],
                'pos': [word.upos for word in sentence.words if len(sentence.words) > 1],
            }
            stanza_objects.append(stanza_object)

        parsed_document = {
            'url': url,
            'stanza': stanza_objects
        }
        parsed_documents.append(parsed_document)

        if i % 10000 == 0:
            print(f"Processed {i} urls..., saving...")
            with open(args.output + f"_{i}" + ".json", 'w', encoding='utf-8') as f:
                json.dump(parsed_documents, f, ensure_ascii=False, indent=4)
    
    print(f"Done serializing {len(parsed_documents)} documents... Saving to path: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(parsed_documents, f, ensure_ascii=False, indent=4)
