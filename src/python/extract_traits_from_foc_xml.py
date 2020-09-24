from lxml import etree
import glob
import pandas as pd


# task: extract the structure width, structure length, etc from the xml files one by one
# pass it a file name, "property name" e.g., achene width, and get back a matrix with rows as species and a column
# containing the data


def parse(file_name):
    parser = etree.XMLParser(remove_blank_text=True)
    parsed_xml = etree.parse(file_name, parser)
    return parsed_xml


def extract_morphology(parsed_xml):
    morphology = parsed_xml.find('description')
    return morphology


def extract_structures(morphology):
    rows = []
    all_statements = morphology.getchildren()
    for index, statement in enumerate(all_statements):
        # print(index)
        structure_all = statement.findall('structure')
        # text_verbatim = statement.find('text').text
        # print("* " + text_verbatim + " *")
        rows.append(pd.Series(extract_structure_names(structure_all)))

    out_df = pd.DataFrame(rows)
    return rows


def extract_structure_names(structure_all):
    for structure_element in structure_all:
        structure = structure_element.attrib['name']
        # parse_all = structure_element.getchildren()
        return(structure)


file_name = "../../data/external/FoCV23/1001.xml"
parsed_xml = parse(file_name)
morphology = extract_morphology(parsed_xml)
test = extract_structures(morphology)
