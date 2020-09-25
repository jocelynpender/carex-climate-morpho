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
        rows.append(extract_structure_names(structure_all))
        #print(extract_structure_names(structure_all))
    #out_df = pd.DataFrame(rows)
    #print(rows)
    return rows


def extract_structure_names(structure_all):
    for structure_element in structure_all:
        structure = structure_element.attrib['name']
        character_all_data = extract_characters(structure_element, structure)
        return(character_all_data)


def extract_characters(structure_element, structure):
    character_all = structure_element.findall('character')
    character_all_data = []
    for character_element in character_all:
        property_name = structure + '_' + character_element.attrib['name']
        property_from = extract_from_to_attribs(character_element, 'from')
        property_to = extract_from_to_attribs(character_element, 'to')
        print([property_name, property_from, property_to])
        character_all_data.append([property_name, property_from, property_to])
    return character_all_data


def extract_from_to_attribs(character_element, from_or_to):
    if 'from' in character_element.attrib:
        return character_element.attrib[from_or_to] + character_element.attrib[from_or_to + '_unit']


file_name = "../../data/external/FoCV23/1001.xml"
parsed_xml = parse(file_name)
morphology = extract_morphology(parsed_xml)
rows = extract_structures(morphology)
