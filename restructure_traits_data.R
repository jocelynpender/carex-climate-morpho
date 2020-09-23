library(tidyverse)

# TODO: figure out how to exclude data inherited from Carex

# import the data frame as a tibble
carex_species_data_frame <- read_csv(file = "data/carex_species_data_frame.csv", col_names = TRUE,
                                     col_types = NULL)
carex_species_data_frame <- rename(carex_species_data_frame, species_name = X1)

collapse_extract_properties <- function(variable_name, list_property_names) {
  # extract and collapse data corresponding to multiple properties
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
# TODO: Carex davisii infloresences 10-25 mm is missing from property list, Carex_xerantica 1.5–5 cm × 5–10 mm; Carex_venusta, 5–100 mm
# Q: Do we include spike within inflorescence data? E.g., Carex basiantha, Carex virescens
inflorescence_length_props <- c("Inflorescence_some_measurement", "Inflorescence_atypical_length", "Inflorescence_length")
inflorescence_length <- collapse_extract_properties("inflorescence_length", inflorescence_length_props)

# Maximum inflorescence width
# Q: Do we include spike within inflorescence data?
# E.g. Spike width, Spike some measurement
inflorescence_width_props <- c("Inflorescence_atypical_width", "Inflorescence_width")
inflorescence_width <- collapse_extract_properties("inflorescence_width", inflorescence_width_props)
# TODO/Q: Do we want to include the atypical measurements? Likely only if they are atypical on the top end.
# Take the highest number regardless.

# Inflorescence complexity (max branch order)
inflorescence_complexity_props <- c()
inflorescence_complexity <- collapse_extract_properties("inflorescence_complexity", inflorescence_complexity_props)

# Maximum fruit length
# TODO: Achene data from Carex_abrupta not appearing in properties
# Achene_atypical_some_measurement, Achene_size, Achene_some_measurement
fruit_length_props <- c("Achene_atypical_length", "Achene_length")
fruit_length <- collapse_extract_properties("fruit_length", fruit_length_props)

# Maximum fruit width
fruit_width_props <- c("Achene_atypical_width", "Achene_width")
fruit_width <- collapse_extract_properties("fruit_width", fruit_width_props)

# TODO: use boxplots to identify outliers and manually verify data.
# TODO: Compare the dataset derived here with my MSc dataset