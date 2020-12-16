import glob
import pandas as pd


from src.python.property_coding_filter import add_property_coding_column, filter_data_frame
from src.python.extract_traits_from_xml import parse, extract_morphology, extract_structures
from src.python.exclude_property_values import exclude_values

# file_name = "../../data/external/FoCV23/1001.xml"
directory = "../../data/external/FNAV23/*.xml"
traits_data_frame = pd.DataFrame([], columns=['property_name', 'from', 'to', 'species_name', 'file_name'])


def format_taxon_id(parsed_xml):
    taxon_id = parsed_xml.find('taxon_identification[@status=\"ACCEPTED\"]')
    genus = taxon_id.find('taxon_name[@rank=\"genus\"]')
    species = taxon_id.find('taxon_name[@rank=\"species\"]')
    return genus.text + '_' + species.text


for file_name in glob.glob(directory):
    print(file_name)
    parsed_xml = parse(file_name)
    species_name = format_taxon_id(parsed_xml)
    morphology = extract_morphology(parsed_xml, morphology_node='description[@type=\"morphology\"]')
    if morphology is not None:
        all_structures_data_frame = extract_structures(morphology, structure_node='biological_entity[@type=\"structure\"]')
        all_structures_data_frame = all_structures_data_frame.assign(species_name=species_name)
        all_structures_data_frame = all_structures_data_frame.assign(file_name=file_name)
        traits_data_frame = traits_data_frame.append(all_structures_data_frame)

property_coding = pd.read_csv("../../data/interim/fna_recode_property_names.csv")

traits_data_frame_with_coding = add_property_coding_column(traits_data_frame, property_coding)
traits_data_frame_with_coding = filter_data_frame(traits_data_frame_with_coding)

# trim semi-colons and nan
traits_data_frame_with_coding = traits_data_frame_with_coding.apply(lambda x: x.replace(";nan", ""), axis=1)

# exclude relative measurements
traits_data_frame_with_coding = exclude_values(traits_data_frame_with_coding, values_to_exclude=['shorter', 'longer', 'lower', 'wider'])

traits_data_frame.to_csv("../../data/processed/fna/fna_traits_data_frame.csv")
traits_data_frame_with_coding.to_csv("../../data/processed/fna/fna_traits_data_frame_with_coding.csv")
