browse_subject_query_url <- function(query_string) {
  # Concatenate a query_string with the http API ask query module URL
  # for the FNA Semantic MediaWiki instance
  base_url <- "http://dev.semanticfna.org/w/api.php?action=browsebysubject&subject="
  url <- paste(base_url, query_string, sep = "")
  return(url)
}
