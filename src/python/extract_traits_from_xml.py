from lxml import etree
import pandas as pd


# task: extract the structure width, structure length, etc from the xml files one by one
# pass it a file name, "property name" e.g., achene width, and get back a matrix with rows as species and a column
# containing the data


def parse(file_name):
    parser = etree.XMLParser(remove_blank_text=True)
    parsed_xml = etree.parse(file_name, parser)
    return parsed_xml


def extract_morphology(parsed_xml, morphology_node='description'):  # = description type="morphology"
    morphology = parsed_xml.find(morphology_node)
    return morphology


def extract_from_to_attribs(character_element, from_or_to):
    if from_or_to in character_element.attrib:
        from_or_to_character_element = character_element.attrib[from_or_to]
        if from_or_to + '_unit' in character_element.attrib:
            from_or_to_character_element = from_or_to_character_element + character_element.attrib[from_or_to + '_unit']
        return from_or_to_character_element


def extract_characters(structure_element, structure):
    character_all = structure_element.findall('character')
    characters_list = []
    if character_all is not None:
        for index, character_element in enumerate(character_all):
            property_name = structure + '_' + character_element.attrib['name']
            property_from = extract_from_to_attribs(character_element, 'from')
            property_to = extract_from_to_attribs(character_element, 'to')
            if property_from is None: # Need more than just the quantitative characters now,
                property_value = character_element.attrib['value'] # looking for branching values
            else:
                property_value = None
            characters_list.append([property_name, property_from, property_to, property_value])
        characters_data_frame = pd.DataFrame(characters_list, columns=["property_name", "from", "to", "value"])
        return characters_data_frame


def extract_structure_names(structure_all):
    structures_data_frame = pd.DataFrame([], columns=["property_name", "from", "to", "value"])
    for structure_element in structure_all:
        structure = structure_element.attrib['name']
        characters_data_frame = extract_characters(structure_element, structure)
        if characters_data_frame.empty is False:
            structures_data_frame = structures_data_frame.append(characters_data_frame, ignore_index=True)
    return structures_data_frame


def extract_structures(morphology, structure_node='structure'): # biological_entity type="structure"
    all_statements = morphology.getchildren()
    all_structures_data_frame = pd.DataFrame([], columns=["property_name", "from", "to", "value"])
    for statement in all_statements:
        structure_all = statement.findall(structure_node)
        characters_data_frame = extract_structure_names(structure_all)
        all_structures_data_frame = all_structures_data_frame.append(characters_data_frame, ignore_index=True)
    return all_structures_data_frame