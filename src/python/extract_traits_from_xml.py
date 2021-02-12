from lxml import etree
import pandas as pd

# task: extract the structure width, structure length, etc from the xml files one by one
# pass it a file name, "property name" e.g., achene width, and get back a matrix with rows as species and a column
# containing the data


extract_traits_into_cols = ["property_name", "property_constraint", "from", "to", "value", "atypical"]


def parse(file_name):
    parser = etree.XMLParser(remove_blank_text=True)
    parsed_xml = etree.parse(file_name, parser)
    return parsed_xml


def extract_morphology(parsed_xml, morphology_node='description'):  # = description type="morphology"
    morphology = parsed_xml.find(morphology_node)
    return morphology


def extract_from_to_attribs(character_element, from_or_to):
    """
    This function is used to either extract "from" attributes or "to" attributes of parent characters. This is the data
    we want from the XML files for our dataset.
    For example, the from="3" or the to="5" seen below:

    <biological_entity id="o20841" name="rhizome" name_original="rhizomes" src="d0_s0" type="structure">
        <character char_type="range_value" from="3" from_unit="mm" name="thickness" src="d0_s0" to="5" to_unit="mm" />
    </biological_entity>

    It will paste the unit on to the from/to measurement to return "3mm" or "5mm" in the above example

    :param character_element: parent node e.g., "rhizome thickness"
    :param from_or_to: either the word "from" or the word "to".
    :return: e.g. "3mm"
    """
    if from_or_to in character_element.attrib:
        from_or_to_character_element = character_element.attrib[from_or_to]
        if from_or_to + '_unit' in character_element.attrib:
            from_or_to_character_element = from_or_to_character_element + character_element.attrib[from_or_to + '_unit']
        return from_or_to_character_element


def extract_characters(structure_element, structure):
    """
    This function extracts character data from a given structure node. It extracts:
    property_name, constraint, property_from, property_to, property_value, atypical

    In this example:

    <biological_entity id="o20843" name="leaf-blade" name_original="leaf-blades" src="d0_s2" type="structure">
        <character char_type="range_value" from="3.5" from_unit="mm" name="width" src="d0_s2" to="8" to_unit="mm" />
      </biological_entity>

      property_name: leaf-blade_width
      constraint:
      property_from: 3.5mm
      property_to: 8mm
      property_value:
      atypical:

    :param structure_element: a biological_entity type="structure" node
    :param structure: the "name" attribute of the structure_element
    :return: a Pandas dataframe with all data that can be extracted from this structure node
    """
    if 'constraint' in structure_element.attrib:
        constraint = structure_element.attrib['constraint']
    else:
        constraint = ''
    character_all = structure_element.findall('character')
    characters_list = []
    if character_all is not None:
        for index, character_element in enumerate(character_all):
            property_name = structure + '_' + character_element.attrib['name']
            property_from = extract_from_to_attribs(character_element, 'from')
            property_to = extract_from_to_attribs(character_element, 'to')
            if property_from is None:  # Need more than just the quantitative characters now,
                property_value = character_element.attrib['value']  # looking for branching values
            else:
                property_value = None

            # add designation if the data is atypical so that these can be filtered out if desired
            if 'to_inclusive' in character_element.attrib:
                atypical = 'atypical'
            elif 'from_inclusive' in character_element.attrib:
                atypical = 'atypical'
            else:
                atypical = ''

            characters_list.append([property_name, constraint, property_from, property_to, property_value, atypical])
        characters_data_frame = pd.DataFrame(characters_list, columns=extract_traits_into_cols)
        return characters_data_frame


def extract_structure_names(structure_all):
    """
    This function runs the structure extraction process over all structure nodes in the file
    :param structure_all: the findall set of all structures biological_entity type="structure"
    :return: a Pandas dataframe with all character data (="properties") for all structures
    """
    structures_data_frame = pd.DataFrame([], columns=extract_traits_into_cols)
    for structure_element in structure_all:
        structure = structure_element.attrib['name']
        characters_data_frame = extract_characters(structure_element, structure)
        if characters_data_frame.empty is False:
            structures_data_frame = structures_data_frame.append(characters_data_frame, ignore_index=True)
    return structures_data_frame


def extract_structures(morphology, structure_node='structure'):  # biological_entity type="structure"
    """
    create an empty dataframe to hold results
    extract all structure nodes from the file
    run the extraction

    :param morphology: node from the xml = description type="morphology"
    :param structure_node: all nodes that have biological_entity type="structure"
    :return:
    """
    all_statements = morphology.getchildren()
    all_structures_data_frame = pd.DataFrame([], columns=extract_traits_into_cols)
    for statement in all_statements:
        structure_all = statement.findall(structure_node)
        characters_data_frame = extract_structure_names(structure_all)
        all_structures_data_frame = all_structures_data_frame.append(characters_data_frame, ignore_index=True)
    return all_structures_data_frame
