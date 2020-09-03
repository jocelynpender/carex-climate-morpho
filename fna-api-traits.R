# Pull data for Carex capitata to ensure API is working as expected
library(devtools)
library(WikipediR)
library(tidyverse)
source_url("https://raw.githubusercontent.com/jocelynpender/fna-query/master/R/src/query.R")

ask_query_titles("[[Taxon name::Carex capitata]]", "carex_capitata.csv")

