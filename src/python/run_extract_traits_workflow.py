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

# sum is used to unnest the reps, https://stackoverflow.com/questions/11860476/how-to-unnest-a-nested-list
collapse_property_coding = pd.DataFrame({'coded_property_name': sum([['maximum_plant_height'] * 5,
                                                                   ['maximum_leaf_width'] * 4,
                                                                   ['maximum_inflorescence_length'] * 3,
                                                                   ['maximum_inflorescence_width']], [])
                                       , 'property_name': ['culm_size', 'culm_height', 'culm_atypical_size',
                                                           'culm_height_or_length', 'culm_length', 'blade_size',
                                                           'blade_width', 'leaf_size', 'leaf_width',
                                                           'inflorescence_height_or_length', 'inflorescence_length',
                                                           'inflorescence_size', 'inflorescence_width']})

carex_traits_collapsed = collapse_traits(carex_traits_data_frame, collapse_property_coding)

# trim semi-colons and nan
carex_traits_collapsed.collapsed_data = carex_traits_collapsed.collapsed_data.apply(lambda x: x.replace(";nan", "").strip(";nan"))

carex_traits_data_frame.to_csv("../../data/processed/foc/carex_traits_data_frame.csv")
carex_traits_collapsed.to_csv("../../data/processed/foc/carex_traits_collapsed.csv")
