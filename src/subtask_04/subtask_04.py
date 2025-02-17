import xml.etree.ElementTree as ET
import pandas as pd

# Parse DrugBank XML and return a list of pathways.
def parse_all_pathways(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    pathways_list = []

    # Loop over each drug element.
    for drug in root.findall("db:drug", ns):
        pathways_elem = drug.find("db:pathways", ns)
        if pathways_elem is not None:
            for pathway in pathways_elem.findall("db:pathway", ns):
                # Get pathway identifier.
                id_elem = pathway.find("db:smpdb-id", ns)
                pathway_id = id_elem.text if id_elem is not None else None

                # Get pathway name.
                name_elem = pathway.find("db:name", ns)
                pathway_name = name_elem.text if name_elem is not None else None

                # Get pathway category.
                cat_elem = pathway.find("db:category", ns)
                pathway_category = cat_elem.text if cat_elem is not None else None

                pathways_list.append({
                    "id": pathway_id,
                    "pathway_name": pathway_name,
                    "category": pathway_category
                })

    return pathways_list

if __name__ == '__main__':
    # Set path to DrugBank XML file.
    file_path = '../drugbank_partial.xml'
    
    # Optional: Uncomment to use the extended XML file.
    # file_path = '../drugbank_partial_and_generated.xml'

    pathways = parse_all_pathways(file_path)
    df_pathways = pd.DataFrame(pathways)

    print(df_pathways)
    # Output the total number of pathways.
    print(f"\nTotal number of pathways: {len(df_pathways)}")