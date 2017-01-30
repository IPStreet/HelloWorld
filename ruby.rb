require 'net/http'
require 'uri'
require 'json'

LIVE_API_KEY = 'LIVE API KEY'

def send_api_request(query)
    endpoint = URI.parse('https://api.ipstreet.com/v2/data/patent')
    http = Net::HTTP.new(endpoint.host, endpoint.port)
    http.use_ssl = true
    request = Net::HTTP::Post.new(endpoint.request_uri)
    request['x-api-key'] = LIVE_API_KEY
    request['Content-Type'] = 'application/json'
    request.body = query.to_json
    response = http.request(request)
    response.body
end

def search_by_owner(owner, page_number)
    query = {'q': {'owner': owner, 'offset': page_number}}
    response = send_api_request(query)
    puts response
end

def get_first_4_pages(owner)
    for page_count in 1..4 do
        response = search_by_owner(owner, page_count)
        puts response
    end
end

def search_claim_only(input)
	query = {'raw_text': '#{input}',
                          'q': {'start_date': '2002-01-01',
                            'start_date_type': 'priority_date',
                            'end_date': '2015-01-01',
                            'end_date_type': 'publication_date',
                            'applied': :true,
                            'granted': :true,
                            'expired': :false,
                            'max_expected_results': 10000}}
    response = send_api_request(query)
    puts response
end


search_by_owner('Microsoft', 1)
get_first_4_pages('Microsoft')

query_text = "a configurable battery pack charging system coupled to said charging system controller, said " \
             "battery pack and a power source, wherein said configurable battery pack charging system charges " \
             "said battery pack in accordance with said battery pack charging conditions set by " \
             "said charging system controller."

search_claim_only(query_text)
