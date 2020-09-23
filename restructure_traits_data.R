library(tidyverse)

# TODO: figure out how to exclude data inherited from Carex

# import the data frame as a tibble
carex_species_data_frame <- read_csv(file = "data/carex_species_data_frame.csv", col_names = TRUE,
                                     col_types = NULL)
carex_species_data_frame <- rename(carex_species_data_frame, species_name = X1)

# extract and collapse data corresponding to multiple properties

collapse_extract_properties <- function(variable_name, list_property_names) {
  variable_tibble <- carex_species_data_frame %>% unite(variable_name, 
                                                        all_of(list_property_names), 
                                                        na.rm = TRUE, remove = FALSE
  ) %>% select(species_name, variable_name)
  return(variable_tibble)
}

# Maximum leaf width
# collapse Blade_width, Leaf_width
# TODO: Deal with Carex species inheriting 0mm;20mm from the Carex genus description
leaf_width_props <- c("Blade_width", "Leaf_width")
leaf_width <- collapse_extract_properties("leaf_width", leaf_width_props)
# How many species are inheriting 0mm;20mm?
num_spp_missing_data <- leaf_width %>% filter(., leaf_width == "0mm;20mm") %>% count
num_spp_missing_data/nrow(carex_species_data_frame) * 100

# Maximum plant height
# No inheritence to worry about here.
culm_height_props <- c("Culm_height", "Culm_some_measurement", "Culm_length", 
                      "Culm_leaf_some_measurement", "Angle_some_measurement")
culm_height <- collapse_extract_properties("culm_height", culm_height_props)
# Q: Do we include flowering length height in this measurement? E.g., Carex davisii 
# Flowering-stem some measurement	

# TODO: Continue going through the empty rows and determine if a property name is missing.
# Stopped at Carex davisii

# Maximum inflorescence length
# TODO: Carex davisii infloresences 10-25 mm is missing from property list
inflorescence_length_props <- c("Inflorescence_some_measurement", "Inflorescence_atypical_length", "Inflorescence_length")
inflorescence_length <- collapse_extract_properties("inflorescence_length", inflorescence_length_props)

# Maximum inflorescence width
# Q: Do we include spike within inflorescence data? I think not. 
# E.g. Spike width, Spike some measurement

# Inflorescence complexity (max branch order)
# Maximum fruit length
# Maximum fruit width