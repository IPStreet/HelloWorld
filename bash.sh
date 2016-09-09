#!/usr/bin/env bash

search_by_owner() {
    # If you have an API key, you can use this method to search for all patents owned by a given company.
    # The method takes an owner name input and page number, returns target page of results from /data/patent

    endpoint="https://api.ipstreet.com/v1/data/patent"

    apiKey="x-api-key:PUT-YOUR-API-KEY-HERE"
    contentType="Content-Type:application/json"

    payload="{'q':{'owner':$1,'offset':$2}}"

    r="curl $endpoint -X POST -H $apiKey -H $contentType -d $payload"
    RESPONSE=`$r`

    # returning response
    echo "$RESPONSE"
}

get_all_pages() {
    # When you want to get all the results of your query, you must loop over all the pages in the given results set
    # This method returns all the results of search_by_owner() method above

    # #first call to get to total_asset_count, insert records to DB
    response=$( search_by_owner $1 1 )

    echo "$response"
    # set total page count
    # Doing some hack to retrieve totalPage value from json response.
    total_page_count=$(echo "$response"| grep -Eo '"totalPage": .*?[^\\]"'| awk '{print $2}'| tr -d '"')

    # follow-on searches to fill data set
    # current_page_count=2  # start at page 2
    for (( current_page_count=2; current_page_count<total_page_count; current_page_count++ ))
    do
        response=$( search_by_owner $1 $current_page_count )

        echo "$response"

        # perform an insert each record into your database here
        echo "$current_page_count pages received"
    done
    echo "$current_page_count total pages received"
}

#########################################
# Uncomment Below to Run Desired function
#########################################

# get just first page of results, print to console
# search_by_owner 'microsoft' 1

# get all results for owner=microsoft, print to console
# get_all_pages 'microsoft'

