library(tidyverse)

# TODO: figure out how to exclude data inherited from Carex

# import the data frame as a tibble
carex_species_data_frame <- read_csv(file = "data/carex_species_data_frame.csv", col_names = TRUE,
                                     col_types = NULL)
carex_species_data_frame <- rename(carex_species_data_frame, species_name = X1)

# Maximum leaf width
# collapse Blade_width, Leaf_width
# TODO: Deal with Carex species inheriting 0mm;20mm from the Carex genus description
leaf_width <- carex_species_data_frame %>% unite("leaf_width", 
                                                 c("Blade_width", "Leaf_width"), 
                                                 na.rm = TRUE, remove = FALSE
                                                 ) %>% select(species_name, 
                                                              leaf_width)
# How many species are inheriting 0mm;20mm?
num_spp_missing_data <- leaf_width %>% filter(., leaf_width == "0mm;20mm") %>% count
num_spp_missing_data/nrow(carex_species_data_frame) * 100

# Maximum plant height
# No inheritence to worry about here.
culm_height_vars <- c("Culm_height", "Culm_some_measurement", "Culm_length", 
                      "Culm_leaf_some_measurement", "Angle some measurement")
culm_height <- carex_species_data_frame %>% unite("culm_height", 
                                                  all_of(culm_height_vars), 
                                                 na.rm = TRUE, remove = FALSE
                                                 ) %>% select(species_name, culm_height)
# Q: Do we include flowering length height in this measurement?
# TODO: Continue going through the empty rows and determine if a property name is missing.
# Stopped at Carex davisii

# Maximum inflorescence length
# Maximum inflorescenc width
# Inflorescence complexity (max branch order)
# Maximum fruit length
# Maximum fruit width