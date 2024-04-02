import json
import argparse
from tqdm import tqdm
from inverted_indexer import save_inverted_index_json


def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments and return the parsed arguments.

    Returns:
        args (Namespace): The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputs', nargs='+', help='List of inverted indices to merge', required=True)
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to the merged index file")
    args = parser.parse_args()  
    return args


if __name__ ==  '__main__':
    args = parse_args()

    indices = []
    merged_index = {}
    for file_path in args.inputs:
        print(f"Merging {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
            for key, value in tqdm(index.items()):
                if key in merged_index:
                    merged_index[key].extend(value)
                else:
                    merged_index[key] = value
    
    print(f"Number of lemmas in inverted index: {len(merged_index.keys())}")
    save_inverted_index_json(merged_index, args.output)