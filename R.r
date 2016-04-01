library(httr)


# A simple Hello World! example which requires no inputs.
#
# Just call hello_world() and a standard concept search query response will be pretty printed to the console.


hello_world<- function(){

    r = POST(url = "https://api.ipstreet.com/v1/sandbox/claim_only",
        add_headers(`x-api-key`="sandbox_api_key"),
        body = list(raw_text= "The quick brown fox jumps over the lazy dog"),
        encode ="json")

    print(content(r))

}

hello_world()
