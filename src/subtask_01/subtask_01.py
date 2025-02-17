import xml.etree.ElementTree as ET
import pandas as pd

# Function to parse the DrugBank XML file and create a DataFrame of pharma products.
def parse_drugbank_xml(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    drugs = []
    
    # Iterate over each drug element.
    for drug in root.findall("db:drug", ns):
        # Unique drug identifier 
        id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        drug_id = id_elem.text if id_elem is not None else None

        # Drug name
        name_elem = drug.find("db:name", ns)
        name = name_elem.text if name_elem is not None else None

        # Drug type
        drug_type = drug.attrib.get("type", None)

        # Drug description
        description_elem = drug.find("db:description", ns)
        description = description_elem.text if description_elem is not None else None

        # Drug state
        state_elem = drug.find("db:state", ns)
        state = state_elem.text if state_elem is not None else None

        # Indications
        indication_elem = drug.find("db:indication", ns)
        indications = indication_elem.text if indication_elem is not None else None

        # Mechanism of action
        mechanism_elem = drug.find("db:mechanism-of-action", ns)
        mechanism = mechanism_elem.text if mechanism_elem is not None else None

        # Food interactions
        food_elem = drug.find("db:food-interactions", ns)
        food_interactions = food_elem.text if food_elem is not None else None

        drugs.append({
            "drug_id": drug_id,
            "name": name,
            "type": drug_type,
            "description": description,
            "state": state,
            "indications": indications,
            "mechanism": mechanism,
            "food_interactions": food_interactions
        })
    return pd.DataFrame(drugs)

if __name__ == '__main__':
    # Path to DrugBank XML file.
    file_path = '../drugbank_partial.xml'

    # Optional: uncomment to use extended DrugBank XML file.
    #file_path = '../drugbank_partial_and_generated.xml'

    # Parse the DrugBank XML file and create a DataFrame.
    df = parse_drugbank_xml(file_path)
    print(df)

    # Optional: Save the DataFrame to a CSV file.
    csv_path = "drug_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"CSV saved as: {csv_path}")