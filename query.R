browse_subject_query_url <- function(query_string) {
  # Concatenate a query_string with the http API ask query module URL
  # for the FNA Semantic MediaWiki instance
  base_url <- "http://dev.semanticfna.org/w/api.php?action=browsebysubject&subject="
  url <- paste(base_url, query_string, sep = "")
  return(url)
}

run_browse_query <- function(query_string) {
  # Run a query against the Semantic MediaWiki http api URL and obtain results back in R
  query_offset = 0
  query_results_list <- list() # Need to initialize the list, then add to it in the loop
  while (!is.null(query_offset) == TRUE) { # While there continues to be an offset...
    url <- browse_subject_query_url(query_string)
    query_results <- query(url, out_class = "none") # Uses the WikipediR query function
    query_results_list[[length(query_results_list) + 1]] <- query_results$query$data
    print(paste("Appending batch", query_offset, "-",
                ifelse(is.null(query_results$`query-continue-offset`), "end", query_results$`query-continue-offset` - 1),
                "to query results")) # Give an indication of progress of the download
    query_offset <- query_results$`query-continue-offset`
  }
  query_results_list <- do.call(c, query_results_list) # Fix up list formatting
  return(query_results_list)
}