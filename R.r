library(httr)

# Utilities for getting results into data frames
ResultsToNewDataframe <- function(results){
  # Loop over content of response, making each a row in your data frame
  patents <-do.call("rbind", content(results)$Assets)
  
  return(as.data.frame(patents)) 
}

ResultsToExistingDataframe <- function(results, existing.data.frame){
  # Append new set of results to an existing data frame of results
  new.data.frame <-ResultsToNewDataframe(results)
  updated.data.frame <- rbind(existing.data.frame,new.data.frame)
  
  
  return(updated.data.frame) 
}

# Example IP Street API calls
SearchByOwner <- function(owner, page.number, api.key){
  r = POST(url = 'https://api.ipstreet.com/v2/data/patent',
           add_headers(`x-api-key` = api.key),
           body = list(q= list(owner = owner, page.number = page.number)),
           encode ="json")
  return(r)
}


GetFirstFourPages <- function(owner, api.key){
  # makes the first request
  r = SearchByOwner(owner = owner, page.number = 1, api.key = api.key)
  
  # create new data frame for results
  patents = ResultsToNewDataframe(r)
  
  # make additional calls for each page
  for (i in 2:4){
    r = SearchByOwner(owner = owner, page.number = i, api.key = api.key)
    #append results to data frame
    patents <- ResultsToExistingDataframe(r,patents)
  }
  return(patents)
}


# Begin program run 
api.key = 'Live_API_Key'

r = SearchByOwner(owner = "microsoft", page.number = 1, api.key = api.key)
single.page.results = ResultsToNewDataframe(r)


first.four.pages.results = GetFirstFourPages(owner = "microsoft", api.key = api.key)

