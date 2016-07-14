import requests
import json


def hello_world_sandbox():
    """ Hello World! example Concept Search API call
    Prints a standard response json object when called.
     """

    endpoint = 'https://api.ipstreet.com/v1/claim_only'
    headers = {'x-api-key': "Live API Key"}
    payload = json.dumps({'raw_text': 'The quick brown fox jumps over the lazy dog'})
    r = requests.post(endpoint, headers=headers, data=payload)

    print(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    return


def search_by_owner(owner, page_number):
    """If you have an API key, you can use this method to search for all patents owned by a given company.
    The method takes an owner name input and page number, returns target page of results from /data/patent
    """
    endpoint = 'https://api.ipstreet.com/v1/data/patent'
    headers = {'x-api-key': 'Live API Key'}
    payload = json.dumps({'q': {'owner': owner, 'offset': page_number}})
    r = requests.post(endpoint, headers=headers, data=payload)

    print(r.text)
    return r.json()


def get_all_pages(owner):
    """When you want to get all the results of your query, you must loop over all the pages in the given results set
    This method returns all the results of search_by_owner() method above
    """

    # #first call to get to total_asset_count, insert records to DB
    response = search_by_owner(owner, 1)

    # set total page count
    total_page_count = response['totalPage']

    # follow-on searches to fill data set
    current_page_count = 2  # start at page 2
    while current_page_count <= total_page_count:
        response = search_by_owner(owner, current_page_count)

        # perform an insert each record into your database here

        print("{} pages received".format(current_page_count))
        current_page_count += 1

    print("{} total pages received".format(current_page_count))


if __name__ == '__main__':
    hello_world_sandbox()  # semantic concept search requiring no inputs

    search_by_owner(owner='microsoft', page_number=1)  # get just first page of results

    get_all_pages(owner='microsoft')  # get all results
