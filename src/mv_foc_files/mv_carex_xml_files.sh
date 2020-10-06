# foc
cd /Users/jocelynpender/fc/fochina/FoCV23/target/final/
cat /Users/jocelynpender/carex-climate-morpho/data/interim/FoCV23_treatment_list.txt | xargs -J % cp % /Users/jocelynpender/carex-climate-morpho/data/external/FoCV23


#fna
cd /Users/jocelynpender/fna/fna-fine-grained-xml/V23/
cat /Users/jocelynpender/carex-climate-morpho/data/interim/FNAV23_treatment_list.txt | xargs -J % cp % /Users/jocelynpender/carex-climate-morpho/data/external/FNAV23

