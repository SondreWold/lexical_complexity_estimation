from tqdm import tqdm
import argparse
import json
import os
import pathlib
import re


def save_nak_json(parsed_urls, parsed_documents, path, nid="all"):
    """
    Save the parsed URLs and documents to a JSON file.

    Parameters:
        parsed_urls (list): A list of parsed URLs.
        parsed_documents (list): A list of parsed documents.
        iterator (str, optional): The iterator value. Defaults to "final".

    Returns:
        None
    """
    with open(path + f"_{nid}.json", 'w', encoding='utf-8') as fp:
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
    parser.add_argument("-i", "--input", type=pathlib.Path, required=True, help="Path to input folder with NAK corpus XML files")
    parser.add_argument("-o", "--output", type=pathlib.Path, required=True, help="Path to output json file")
    parser.add_argument("-s", "--single", action='store_true')
    parser.add_argument("-n", "--nid", type=str, required=False, help="Newspaper identifier")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    print("---- NAK raw document parser ---- ")
    args = parse_args()
    error_parse = 0
    parsed_documents = []
    parsed_urls = []
    error_length = 0

    directory = os.fsencode(args.input)
    for file in os.listdir(directory):
        subfolder = os.fsdecode(file)
        if subfolder.endswith(".tar.gz") or subfolder.endswith(".DS_Store") or subfolder.endswith(".json"):
            continue
        if args.single:
            if subfolder.split("-")[0] != args.nid:
                continue

        path = args.input + f'/{subfolder}'
        print(f"Parsing {path}...")
        for file in tqdm(os.listdir(os.fsencode(args.input + f'/{subfolder}'))):
            xml_filename = path + "/" + file.decode()
            with open(xml_filename, "r") as xml:
                input = xml.read()
            try:
                document = re.findall("<body>(.*?)</body>", input, re.DOTALL)[0]
                santized_document = re.sub(
                    '<[^<]+?>', '', document).replace('\r', '')  # Remove HTML tags
            except Exception:
                error_parse += 1
                continue
            
            if len(santized_document) < 1000:
                error_length += 1
                continue
            
            parsed_documents.append(santized_document)
            parsed_urls.append(xml_filename)
            
    print("Finished parsing...")
    print(f"json parse errors = {error_parse}")
    print(f"length errors = {error_length}")
    print(f'Number of documents = {len(parsed_documents)}')
    save_nak_json(parsed_urls, parsed_documents, args.output, nid=args.nid)
