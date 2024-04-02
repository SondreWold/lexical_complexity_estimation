import argparse
import json
import os
import pathlib
import re
import unicodedata


def save_st_json(parsed_urls, parsed_documents, path):
    """
    Save the parsed URLs and documents to a JSON file.

    Parameters:
        parsed_urls (list): A list of parsed URLs.
        parsed_documents (list): A list of parsed documents.
        iterator (str, optional): The iterator value. Defaults to "final".

    Returns:
        None
    """
    with open(path, 'w', encoding='utf-8') as fp:
        out = {
                'urls': parsed_urls,
                'documents': parsed_documents
            }
        json.dump(out, fp, ensure_ascii=False)


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        args (Namespace): The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=pathlib.Path, required=True, help="Path to input folder with ST corpus XML files")
    parser.add_argument("-o", "--output", type=pathlib.Path, required=True, help="Path to output json file")
    args = parser.parse_args()
    return args


def flatten(ndict):
    def key_value_pairs(d, key=[]):
        if not isinstance(d, dict):
            yield tuple(key), d
        else:
            for level, d_sub in d.items():
                key.append(level)
                yield from key_value_pairs(d_sub, key)
                key.pop()
    return dict(key_value_pairs(ndict))


if __name__ == '__main__':
    print("---- ST raw document parser ---- ")
    args = parse_args()
    print(args)
    error_parse = 0
    parsed_documents = []
    parsed_urls = []
    error_length = 0

    directory = os.fsencode(args.input)
    for file in os.listdir(directory):
        with open(args.input + "/" + file.decode(), "r", encoding='utf-8') as xml:
            document = xml.read()
            santized_document = re.sub(
                    '<[^<]+?>', '', document).replace('\r', '')  # Remove HTML tags
            santized_document = re.sub(r'\n+', '\n', santized_document).strip()
            d = []
            for element in santized_document.split('\n')[5:]:
                if len(element) < 2:
                    continue
                else:
                    d.append(element)
            final_doc = ' '.join(d)
            final_doc = final_doc.encode('utf-8', 'ignore').decode("utf-8").replace('\t', '').replace('\n', '')
            final_doc = re.sub(' +', ' ', final_doc)
            final_doc = unicodedata.normalize("NFKD", final_doc)
            parsed_documents.append(final_doc)
            parsed_urls.append(file.decode())

    print("Finished parsing...")
    print(f"json parse errors = {error_parse}")
    print(f"length errors = {error_length}")
    print(f'Number of documents = {len(parsed_documents)}')
    save_st_json(parsed_urls, parsed_documents, args.output)
