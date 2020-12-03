

def collapse_traits(carex_data_frame, coded_property_name_df, sep_property_data=";", include_from = False):
    """
    # Add column called 'coded_property_name' and create a function to group data together based on the coding

    Based on a coding of property names, e.g.,
    # Maximum plant height =
    # culm_size, culm_height, culm_atypical_size, culm_height_or_length, culm_length

    aggregate properties and property values by concatenating with join (values pasted together with a sep_value)
    so that properties are "re-coded" into new propery bins

    :param include_from:
    :param sep_property_data:
    :param sep_from_to:
    :param carex_data_frame: Pandas dataframe containing columns "property_name", "from", "to", "species_name"
    :param coded_property_name_df: a coding dataframe that identifies what the new property name for each property
    should be, with columns "coded_property_name" (i.e., new name) and "property_name" (i.e., old name)
    :return: coded_carex_collapsed: cleaned, aggregated pandas dataframe with species_name, coded_property_name and
    pasted values
    """
    coded_carex_data_frame = carex_data_frame.set_index('property_name').\
        join(coded_property_name_df.set_index('property_name')) # add coded_property name as a column in a new data
    # frame

    if include_from:
        coded_carex_data_frame['collapsed_data_minimum'] = coded_carex_data_frame['from'].astype(str)
        coded_carex_data_frame['collapsed_data_maximum'] = coded_carex_data_frame.to.astype(str)
        collapsed_data_cols = ['collapsed_data_minimum', 'collapsed_data_maximum']
    else:
        coded_carex_data_frame['collapsed_data'] = coded_carex_data_frame.to.astype(str)
        collapsed_data_cols = ['collapsed_data']

    collapsed_data_cols.extend(['coded_property_name', 'species_name'])
    coded_carex_data_frame = coded_carex_data_frame[collapsed_data_cols] # filter the data frame to only the collapsed data values

    if include_from:
        coded_carex_maximum = coded_carex_data_frame[coded_carex_data_frame.collapsed_data_maximum != "nan"] \
            [['species_name', 'coded_property_name', 'collapsed_data_maximum']] # remove string 'nan' values
        coded_carex_maximum = coded_carex_maximum.groupby(['species_name', 'coded_property_name']) \
            ['collapsed_data_maximum'].apply(sep_property_data.join).reset_index()
        coded_carex_minimum = coded_carex_data_frame[coded_carex_data_frame.collapsed_data_minimum != "nan"] \
            [['species_name', 'coded_property_name', 'collapsed_data_minimum']]  # remove string 'nan' values
        coded_carex_minimum = coded_carex_minimum.groupby(['species_name', 'coded_property_name']) \
            ['collapsed_data_minimum'].apply(sep_property_data.join).reset_index()
        coded_carex_collapsed = coded_carex_maximum.merge(coded_carex_minimum, how='outer')
    else:

        # https://stackoverflow.com/questions/59022050/using-pandas-groupby-to-collapse-rows-into-a-single-row
        coded_carex_collapsed = coded_carex_data_frame.groupby(['species_name', 'coded_property_name'])\
            ['collapsed_data'].apply(sep_property_data.join).reset_index() # paste all the data together per species and
        # per new property name, including multiples, if they exist.


    return coded_carex_collapsed
