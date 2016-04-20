package main

import (
    "bytes"
    "fmt"
    "net/http"
    "io/ioutil"
)

func main() {
    url := "https://api.ipstreet.com/v1/sandbox/claim_only"
    fmt.Println("URL:>", url)

    var raw_text_query = []byte(`{"raw_text": "The quick brown fox jumps over the lazy dog"}`)
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(raw_text_query))
    req.Header.Set("x-api-key", "sandbox_api_key")
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }

    defer resp.Body.Close()

    fmt.Println("response Status:", resp.Status)
    fmt.Println("response Headers:", resp.Header)


    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println("response Body:", string(body))
}
