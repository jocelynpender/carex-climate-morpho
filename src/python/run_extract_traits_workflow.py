import glob
import pandas as pd
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

carex_traits_data_frame.to_csv("../../data/processed/carex_traits_data_frame.csv")
