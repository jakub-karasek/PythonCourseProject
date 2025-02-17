import xml.etree.ElementTree as ET
import pandas as pd
import requests

# Return stripped text from a subelement.
def get_text(elem, tag, ns={'db': 'http://www.drugbank.ca'}):
    subelem = elem.find(tag, ns)
    return subelem.text.strip() if subelem is not None and subelem.text else None

# Return UniProt ID from a drug XML element.
def get_uniprot_id(drug, ns={'db': 'http://www.drugbank.ca'}):
    targets = drug.find("db:targets", ns)
    if targets is None:
        return ""
    for target in targets.findall("db:target", ns):
        polypep = target.find("db:polypeptide", ns)
        if polypep is not None:
            ext_ids = polypep.find("db:external-identifiers", ns)
            if ext_ids is not None:
                for ext in ext_ids.findall("db:external-identifier", ns):
                    resource = get_text(ext, "db:resource", ns)
                    if resource == "UniProtKB":
                        return get_text(ext, "db:identifier", ns) or ""
    return ""

# Fetch UniProt details for a given ID.
def fetch_uniprot_details(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            xml_filename = f"uniprot_drug_data.xml"
            with open(xml_filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Downloaded XML saved as: {xml_filename}")
            ns_up = {"up": "http://uniprot.org/uniprot"}
            root = ET.fromstring(response.text)
            function = ""
            for comment in root.findall("up:entry/up:comment[@type='function']", ns_up):
                text_elem = comment.find("up:text", ns_up)
                if text_elem is not None and text_elem.text:
                    function = text_elem.text.strip()
                    break
            subcellular = ""
            for comment in root.findall("up:entry/up:comment[@type='subcellular location']", ns_up):
                text_elem = comment.find("up:text", ns_up)
                if text_elem is not None and text_elem.text:
                    subcellular = text_elem.text.strip()
                    break
            return {"function": function, "subcellular_location": subcellular}
        else:
            return {"function": "", "subcellular_location": ""}
    except Exception as e:
        print(f"Error fetching UniProt details for {uniprot_id}: {e}")
        return {"function": "", "subcellular_location": ""}

# Parse the DrugBank XML file and create a DataFrame containing:
#  - drug_id, name, type, description, state,
#  - indications, mechanism, food_interactions,
#  - uniprot_id
def parse_drugbank_xml(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    drugs = []
    
    for drug in root.findall("db:drug", ns):
        # Unique drug identifier
        id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        drug_id = id_elem.text.strip() if id_elem is not None and id_elem.text else None

        # Drug name
        name_elem = drug.find("db:name", ns)
        name = name_elem.text.strip() if name_elem is not None and name_elem.text else None

        # Drug type
        drug_type = drug.attrib.get("type", None)

        # Drug description (replace newlines with spaces)
        description_elem = drug.find("db:description", ns)
        description = (description_elem.text.strip().replace("\n", " ") 
                       if description_elem is not None and description_elem.text else None)

        # Drug state
        state_elem = drug.find("db:state", ns)
        state = state_elem.text.strip() if state_elem is not None and state_elem.text else None

        # Indications for use
        indication_elem = drug.find("db:indication", ns)
        indications = indication_elem.text.strip() if indication_elem is not None and indication_elem.text else None

        # Mechanism of action (replace newlines with spaces)
        mechanism_elem = drug.find("db:mechanism-of-action", ns)
        mechanism = (mechanism_elem.text.strip().replace("\n", " ") 
                     if mechanism_elem is not None and mechanism_elem.text else None)

        # Food interactions
        food_elem = drug.find("db:food-interactions", ns)
        food_interactions = food_elem.text.strip() if food_elem is not None and food_elem.text else None

        # UniProt ID – get it from targets/polypeptide/external-identifiers, if available
        uniprot_id = get_uniprot_id(drug, ns)
        
        drugs.append({
            "drug_id": drug_id,
            "name": name,
            "type": drug_type,
            "description": description,
            "state": state,
            "indications": indications,
            "mechanism": mechanism,
            "food_interactions": food_interactions,
            "uniprot_id": uniprot_id
        })
    
    return pd.DataFrame(drugs)

if __name__ == '__main__':
    file_path = '../drugbank_partial.xml'
    # Optional: Uncomment to use extended DrugBank XML file.
    file_path = '../drugbank_partial_and_generated.xml'
    target_drugbank_id = input("Enter drugbank id: ").strip()
    
    df = parse_drugbank_xml(file_path)
    df_filtered = df[df['drug_id'] == target_drugbank_id]
    
    if df_filtered.empty:
        print(f"No drug found with drugbank id: {target_drugbank_id}")
    else:
        details_list = []
        for idx, row in df_filtered.iterrows():
            uniprot_id = row.get("uniprot_id", "")
            if uniprot_id:
                print(f"Fetching UniProt data for {uniprot_id} ...")
                uniprot_details = fetch_uniprot_details(uniprot_id)
            else:
                uniprot_details = {"function": "", "subcellular_location": ""}
            details_list.append(uniprot_details)
        
        df_details = pd.DataFrame(details_list)
        df_filtered = pd.concat([df_filtered.reset_index(drop=True), df_details], axis=1)
        
        print("\n========================================")
        print("Detailed drug data:")
        print("========================================")
        for _, row in df_filtered.iterrows():
            print(f"DrugBank ID             : {row['drug_id']}")
            print(f"Drug Name               : {row['name']}")
            print(f"Drug Type               : {row['type']}")
            print(f"Description             : {row['description']}")
            print(f"State                   : {row['state']}")
            print(f"Indications             : {row['indications']}")
            print(f"Mechanism               : {row['mechanism']}")
            print(f"Food Interactions       : {row['food_interactions']}")
            print(f"UniProt ID              : {row['uniprot_id']}")
            print(f"Function                : {row.get('function', '')}")
            print(f"Subcellular Location    : {row.get('subcellular_location', '')}")
            print("========================================\n")
        
        csv_path = "drug_data_with_uniprot_details.csv"
        df_filtered.to_csv(csv_path, index=False)
        print(f"CSV saved as: {csv_path}")
