from parser_utils import save_json
from tqdm import tqdm
from typing import List
import re
import requests
import time


def get_sitemap_from_list(xml_path: str) -> List[str]:
    """Retrieves a list of URLs from an XML sitemap file.

    Args:
        xml_path (str): The path to the XML sitemap file.

    Returns:
        List[str]: A list of URLs extracted from the XML sitemap file.
    """
    with open(xml_path, "r") as xml:
        f = xml.read()
        # Skipping articles from NBL (bigoraphy lexicon)
        x = re.findall(r'(https://snl.no/[\w]+)', f)
        print(f"Found {len(x)} articles in sitemap...")
        return x


if __name__ == '__main__':
    print("---- SNL sitemap parser and fetcher! ---- ")
    urls = get_sitemap_from_list("sitemap.xml")
    error_404 = 0
    error_json_parse = 0
    parsed_documents = []
    parsed_urls = []
    for iterator, url in (enumerate(tqdm(urls))):
        time.sleep(1)
        topic = url.split("/")[-1].replace('_', ' ')
        try:
            print(f"Fetching: {url}")
            response = requests.get(f'{url}.json', headers={
                                    'Accept': 'application/json'})
            if response.status_code == 404:
                error_404 += 1
                continue
            try:
                document = response.json().get('xhtml_body')
                santized_document = topic + " " + re.sub(
                    '<[^<]+?>', '', document).replace('\r', '')  # Remove HTML tags
                parsed_documents.append(santized_document)
                parsed_urls.append(url)
            except Exception:
                error_json_parse += 1

            if iterator % 5000 == 0:
                print(f"Processed {iterator} urls..., saving...")
                save_json(parsed_urls, parsed_documents, iterator)

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    print("Finished parsing...")
    print(f"404 errors = {error_404}")
    print(f"json parse errors = {error_json_parse}")
    save_json(parsed_urls, parsed_documents)
