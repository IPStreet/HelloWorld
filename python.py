import requests
import json


def search_by_owner(owner, page_number, api_key):
    """If you have an API key, you can use this method to search for all patents owned by a given company.
    The method takes an owner name input and page number, returns target page of results from /data/patent
    """
    endpoint = 'https://api.ipstreet.com/v3/patent_data'
    headers = {'x-api-key': api_key}
    payload = json.dumps({'q': {'current_owner': owner, 'page': page_number}})
    r = requests.post(endpoint, headers=headers, data=payload)

    print(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')))  # pretty prints results
    return r.json()


def get_first_4_pages(owner, api_key):
    """When you want to get all the results of your query, you must loop over all the pages in the given results set
    This method returns first 4 pages of search_by_owner() method above
    """

    # #first call to get to total_asset_count, insert records to DB
    response = search_by_owner(owner, 1, api_key)

    # set total page count
    total_page_count = int(response['total_pages'])

    # follow-on searches to fill data set
    current_page_count = 2  # start at page 2
    while current_page_count <= 4:
        response = search_by_owner(owner, current_page_count, api_key)

        # perform an insert each record into your database here

        print('{} pages received'.format(current_page_count))
        current_page_count += 1


def search_claim_only(input, api_key):
    """If you have an API key, you can use this method to search for patents conceptually similar to your given input
    The method takes a raw text input and returns the first page of results from /semantic_search'"""
    endpoint = 'https://api.ipstreet.com/v3/semantic_search'
    headers = {'x-api-key': api_key}
    payload = json.dumps({'raw_text': str(input),
                          "index_type": "claim_only",
                          'q': {'grant_date_start': '2002-01-01',
                                'publication_end_date': '2015-01-01',
                                'applied': True,
                                'granted': True,
                                'expired': False,
                                'max_expected_results': 10000}})
    r = requests.post(endpoint, headers=headers, data=payload)

    print(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')))  # pretty prints results


def download_description_text(text_description_link, api_key):
    """Downloads the XML version of given patents description text"""
    endpoint = text_description_link
    headers = {'x-api-key': api_key}

    r = requests.get(endpoint, headers=headers)
    print(r.text)
    return r.text


if __name__ == '__main__':

    Live_API_Key = 'Live_API_Key'

    # get just first page of results, print to console
    search_by_owner(owner='microsoft', page_number=1, api_key=Live_API_Key)

    # get first 4 pages of results for owner=microsoft, print to console
    get_first_4_pages(owner='microsoft', api_key=Live_API_Key)

    # Concept search at the /claim_only/ endpoint for the input string, print to console
    query_text = "a configurable battery pack charging system coupled to said charging system controller, said " \
                 "battery pack and a power source, wherein said configurable battery pack charging system charges " \
                 "said battery pack in accordance with said battery pack charging conditions set by " \
                 "said charging system controller."
    search_claim_only(query_text, api_key=Live_API_Key)

    # download and print the description text for the first 5 patents owned by microsoft
    results = search_by_owner(owner='microsoft', page_number=1, api_key=Live_API_Key)
    for asset in results['assets'][:5]:
        download_description_text(asset['text_description_link'], Live_API_Key)
