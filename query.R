browse_subject_query_url <- function(query_string) {
  # Concatenate a query_string with the http API browse by subject module URL
  # for the FNA Semantic MediaWiki instance
  base_url <- "http://dev.semanticfna.org/w/api.php?action=browsebysubject&subject="
  url <- paste(base_url, query_string, sep = "")
  return(url)
}

run_browse_query <- function(query_string) {
  # Run a query against the Semantic MediaWiki http api URL and obtain results back in R
  # This function is VERY conserved. It was taken from the run_ask_query function in the fna-query GitHub repo
  # TODO: merge this function with the existing function to be multi-purpose
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

clean_species_property <- function(species_property) {
  # This function is used to clean up the data returned by the browsebysubject API via the WikipediR query function call
  # The data returned is highly nested, using lists as the main data structure
  # This function is used to flatten the hierarchical list nesting and retrieve only what is useful: property name and value
  # ------
  # Input: List of length 2, with $property = property name and $dataitem = List of 1 (containing a List of 2, with type & property value)
  # The input is one "list item" from the returned result set query_results_list
  # Output: A vector with names. Each value in the vector is a concatenated set of property values (i.e., if there
  # are more than one value for a property, they are concatenated with ";"). The names of the vector are the 
  # property names
  # ------
  species_property <- species_property %>% unlist
  species_property_vector <- vector()
  data_items <- species_property %>% .[names(.) == "dataitem.item"]
  species_property_vector[1] <- paste(data_items, sep="", collapse=";") 
  names(species_property_vector) <- species_property['property']
  return(species_property_vector)
}