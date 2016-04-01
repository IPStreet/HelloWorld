import requests
import json

"""
A simple Hello World! example which requires no inputs.

Just call hello_world() and a standard concept search query response will be pretty printed to the console.
"""


def hello_world():
    """ Hello World! example Concept Search API call
    Prints a standard response json object when called """

    endpoint = 'https://api.ipstreet.com/v1/sandbox/claim_only'
    headers = {'Authorization': 'sandbox_api_key'}
    payload = json.dumps({'raw_text': 'The quick brown fox jumps over the lazy dog'})
    r = requests.post(endpoint, headers=headers, data=payload)

    print(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')))
    return


if __name__ == '__main__':
    hello_world()
