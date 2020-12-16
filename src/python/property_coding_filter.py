import pandas as pd


def add_property_coding_column(traits_data_frame, property_coding):
    """
    add coding column
    :param traits_data_frame:
    :param property_coding:
    :return:
    """
    traits_data_frame = traits_data_frame.set_index('property_name'). \
        join(property_coding.set_index('property_name'))
    return traits_data_frame


def filter_data_frame(traits_data_frame):
    traits_data_frame = traits_data_frame[traits_data_frame.coded_property_name.notnull()]
    traits_data_frame = traits_data_frame[['species_name', 'coded_property_name', 'property_constraint', 'from',
                                           'to', 'value', 'atypical']].reset_index()
    return traits_data_frame

