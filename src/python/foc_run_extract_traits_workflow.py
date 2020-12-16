import glob
import pandas as pd

from src.python.collapse_traits_from_xml import collapse_traits
from src.python.extract_traits_from_xml import parse, extract_morphology, extract_structures

# file_name = "../../data/external/FoCV23/1001.xml"
directory = "../../data/external/FoCV23/*.xml"
traits_data_frame = pd.DataFrame([], columns=['property_name', 'property_constraint', 'from', 'to', 'species_name', 'file_name'])


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
        traits_data_frame = traits_data_frame.append(all_structures_data_frame)

collapse_property_coding = pd.read_csv("../../data/interim/foc_recode_property_names.csv")

traits_collapsed = collapse_traits(traits_data_frame, collapse_property_coding, include_from=True)

# trim semi-colons and nan
traits_collapsed = traits_collapsed.apply(lambda x: x.replace(";nan", ""), axis=1)

traits_data_frame.to_csv("../../data/processed/foc/foc_traits_data_frame.csv")
traits_collapsed.to_csv("../../data/processed/foc/foc_traits_collapsed.csv")
