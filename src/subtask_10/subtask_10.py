import xml.etree.ElementTree as ET
import pandas as pd

# Parse DrugBank XML and extract drug interactions information.
def parse_drug_interactions(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Build a mapping from DrugBank ID to the drug's official name.
    drug_name_mapping = {}
    for drug in root.findall('.//db:drug', ns):
        primary_id_elem = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id_elem is None or not primary_id_elem.text:
            primary_id_elem = drug.find('db:drugbank-id', ns)
        drugbank_id = primary_id_elem.text.strip() if primary_id_elem is not None and primary_id_elem.text else None

        name_elem = drug.find('db:name', ns)
        drug_name = name_elem.text.strip() if name_elem is not None and name_elem.text else None

        if drugbank_id:
            drug_name_mapping[drugbank_id] = drug_name

    interactions_data = []
    # Iterate again to process interactions.
    for drug in root.findall('.//db:drug', ns):
        primary_id_elem = drug.find('db:drugbank-id[@primary="true"]', ns)
        if primary_id_elem is not None and primary_id_elem.text:
            drugbank_id = primary_id_elem.text.strip()
        else:
            drugbank_id = drug.find('db:drugbank-id', ns).text.strip() if drug.find('db:drugbank-id', ns) is not None else None

        # Get the official name for this main drug.
        drug_official_name = drug_name_mapping.get(drugbank_id)

        interactions_elem = drug.find('db:drug-interactions', ns)
        if interactions_elem is not None:
            for interaction in interactions_elem.findall('db:drug-interaction', ns):
                # Get interacting drug info from attributes.
                inter_drugbank_id = interaction.attrib.get('drugbank-id')
                inter_drug_name = interaction.attrib.get('name')
                
                # If attributes are not available, try to get them from child elements.
                if not inter_drugbank_id:
                    id_elem = interaction.find('db:drugbank-id', ns)
                    inter_drugbank_id = id_elem.text.strip() if (id_elem is not None and id_elem.text) else None
                if not inter_drug_name:
                    name_elem = interaction.find('db:name', ns)
                    inter_drug_name = name_elem.text.strip() if (name_elem is not None and name_elem.text) else None

                desc_elem = interaction.find('db:description', ns)
                description = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else None

                interactions_data.append({
                    "DrugBank_ID": drugbank_id,
                    "Drug_Official_Name": drug_official_name,
                    "Interacting_DrugBank_ID": inter_drugbank_id,
                    "Interacting_Drug_Name": inter_drug_name,
                    "Description": description
                })

    return pd.DataFrame(interactions_data)

if __name__ == "__main__":
    file_path = '../drugbank_partial.xml'
    df_interactions = parse_drug_interactions(file_path)
    
    # Display the DataFrame containing drug interaction information.
    print(df_interactions)
    
    # Optionally, save the DataFrame to a CSV file.
    df_interactions.to_csv('drug_interactions.csv', index=False)
