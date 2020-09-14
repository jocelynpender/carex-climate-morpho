# Pull data for Carex capitata to ensure API is working as expected
library(devtools)
library(WikipediR)
library(tidyverse)
source_url("https://raw.githubusercontent.com/jocelynpender/fna-query/master/R/src/query.R")
# Need to add scripts to access the API browse module
# For now, develop some utilitarian code in this repo
source('query.R')

carex_species_checklist <- ask_query_titles('[[Category:Carex]][[Taxon rank::species]]', 'data/carex_species.csv')

carex_species_data <- list()
for (carex_species in carex_species_checklist) {
  species_data_list <- run_browse_query(carex_species) # pull all property data for each carex species
  collapsed_species_data <- lapply(species_data_list, clean_species_property) %>% unlist
  carex_species_data[[carex_species]] <- collapsed_species_data
}

carex_species_data_frame <- bind_rows(carex_species_data)
rownames(carex_species_data_frame) <- carex_species_checklist
write.csv(carex_species_data_frame, file = "data/carex_species_data_frame.csv")