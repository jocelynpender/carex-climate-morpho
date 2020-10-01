import glob
import pandas as pd

from src.python.collapse_traits_from_foc_xml import collapse_traits
from src.python.extract_traits_from_foc_xml import parse, extract_morphology, extract_structures

# file_name = "../../data/external/FoCV23/1001.xml"
directory = "../../data/external/FoCV23/*.xml"
carex_traits_data_frame = pd.DataFrame([], columns=['property_name', 'from', 'to', 'species_name', 'file_name'])


def format_taxon_id(parsed_xml):
    taxon_id = parsed_xml.find('TaxonIdentification[@Status=\"ACCEPTED\"]')
    genus = taxon_id.find('genus_name')
    species = taxon_id.find('species_name')
    return genus.text + '_' + species.text


for file_name in glob.glob(directory):
    print(file_name)
    parsed_xml = parse(file_name)
    species_name = format_taxon_id(parsed_xml)
    morphology = extract_morphology(parsed_xml)
    if morphology is not None:
        all_structures_data_frame = extract_structures(morphology)
        all_structures_data_frame = all_structures_data_frame.assign(species_name=species_name)
        all_structures_data_frame = all_structures_data_frame.assign(file_name=file_name)
        carex_traits_data_frame = carex_traits_data_frame.append(all_structures_data_frame)

coded_property_name_df = pd.DataFrame({'coded_property_name': ['maximum_plant_height'] * 5
                                       , 'property_name': ['culm_size', 'culm_height', 'culm_atypical_size',
                                                           'culm_height_or_length', 'culm_length']})

coded_carex_traits_collapsed = collapse_traits(carex_traits_data_frame, coded_property_name_df)

carex_traits_data_frame.to_csv("../../data/processed/carex_traits_data_frame.csv")
coded_carex_traits_collapsed.to_csv("coded_carex_traits_collapsed.csv")

# Maximum plant height
# culm_size, culm_height, culm_atypical_size, culm_height_or_length, culm_length

# - Maximum leaf width
# blade_size, blade_width, leaf_size, leaf_width

# - Maximum inflorescence length
# inflorescence_height_or_length, inflorescence_length, inflorescence_size

# - Maximum inflorescence width
# inflorescence_width, inflorescence_size?? (but already used in inflorescence length)

# - Inflorescence complexity (max branch order)

# - Maximum fruit length
# Nothing??

# - Maximum fruit width
# Nothing??

