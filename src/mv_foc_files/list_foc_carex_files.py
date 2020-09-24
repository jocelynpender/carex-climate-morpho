#!/usr/bin/env python
# coding: utf-8

# In[36]:


from __future__ import print_function
import sys
import glob
from lxml import etree

#file = sys.argv[1]
#file = '../../../coarse_grained_fna_xml/V2/V2_134.xml'
for volume_path in glob.glob("/Users/jocelynpender/fc/fochina/FoCV23"):
    volume = volume_path.split("/")[-1]
#volume = "25"
    my_file=open("/Users/jocelynpender/fc/fochina/FoCV23/" + volume +                  "_treatment_list.txt","w")
    for file_name in sorted(glob.glob("/Users/jocelynpender/fc/fochina/FoC2-5.13-25/FoCV23/*.xml")):
        tree = etree.parse(file_name)
        # define root
        root = tree.getroot()
        # find ACCEPTED taxon_indentification:

        for taxon_identification in root.findall("./TaxonIdentification/[@Status='ACCEPTED']"):
            # find all taxon_name under ACCEPTED taxon_identification
            for taxon_name in taxon_identification.findall('./genus_name'):
                print(taxon_name.text + "," + file_name)
                if taxon_name.text == "Carex":
                    file_name = file_name.split('/')[-1] 
                    my_file.write(file_name+'\n')

    my_file.close()


# In[ ]:




