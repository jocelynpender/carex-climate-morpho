

def collapse_traits(carex_data_frame, coded_property_name_df, sep_property_data=";", include_from = False, sep_from_to = ","):
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
        coded_carex_data_frame['collapsed_data'] = coded_carex_data_frame.loc[:, ['from', 'to']].apply(
            lambda x: sep_from_to.join(x.dropna().astype(str)), axis=1) # collapse "from" and "to" using pandas groupby and
        # apply with join
    else:
        coded_carex_data_frame['collapsed_data'] = coded_carex_data_frame.to.astype(str)

    coded_carex_data_frame = coded_carex_data_frame[['coded_property_name', 'species_name', 'collapsed_data']] #
    # filter the data frame to only the collapsed data values

    coded_carex_collapsed = coded_carex_data_frame.groupby(['species_name', 'coded_property_name'])\
        ['collapsed_data'].apply(sep_property_data.join).reset_index() # paste all the data together per species and
    # per new property name, including multiples, if they exist.

    return coded_carex_collapsed