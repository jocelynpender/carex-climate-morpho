# exclude things like "shorter" and "longer" - any value that includes these should be excluded

def exclude_values(traits_data_frame, values_to_exclude):
    for value_to_exclude in values_to_exclude:
        traits_data_frame = traits_data_frame[~traits_data_frame['value'].str.contains(value_to_exclude, na=False)]
    return traits_data_frame

# filtered_traits_data_frame = exclude_values(traits_data_frame, values_to_exclude=['shorter', 'longer'])