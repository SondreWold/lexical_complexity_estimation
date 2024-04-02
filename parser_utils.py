import json


def save_json(parsed_urls, parsed_documents, iterator="final"):
    """
    Save the parsed URLs and documents to a JSON file.

    Parameters:
        parsed_urls (list): A list of parsed URLs.
        parsed_documents (list): A list of parsed documents.
        iterator (str, optional): The iterator value. Defaults to "final".

    Returns:
        None
    """
    with open(f'./snl_data2/documents_{iterator}.json', 'w', encoding='utf-8') as fp:
                    out = {
                        'urls': parsed_urls,
                        'documents': parsed_documents
                    }
                    json.dump(out, fp, ensure_ascii=False)