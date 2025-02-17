import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Parse DrugBank XML and return a list of pathways records.
def parse_all_pathways(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    pathways_list = []

    # Loop over each drug in the XML.
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

                # Collect associated drug IDs and names.
                drug_ids = []
                drug_names = []
                drugs_elem = pathway.find("db:drugs", ns)
                if drugs_elem is not None:
                    for drug_item in drugs_elem.findall("db:drug", ns):
                        d_id_elem = drug_item.find("db:drugbank-id", ns)
                        d_name_elem = drug_item.find("db:name", ns)
                        if d_id_elem is not None:
                            drug_ids.append(d_id_elem.text)
                        if d_name_elem is not None:
                            drug_names.append(d_name_elem.text)

                pathways_list.append({
                    "id": pathway_id,
                    "pathway_name": pathway_name,
                    "category": pathway_category,
                    "drug_ids": drug_ids,
                    "drug_names": drug_names
                })

    return pathways_list

# Build a mapping from drug to count of associated pathways.
def build_drug_pathway_counts(pathways):
    drug_to_pathways = {}

    # Loop over each pathway record.
    for record in pathways:
        p_identifier = record.get("pathway_name")
        # Add pathway name for each drug in the record.
        for drug in record.get("drug_names", []):
            if drug:
                if drug not in drug_to_pathways:
                    drug_to_pathways[drug] = set()
                drug_to_pathways[drug].add(p_identifier)

    drug_counts = {drug: len(pathways) for drug, pathways in drug_to_pathways.items()}
    return drug_counts

# Display a histogram of the number of pathways per drug.
def display_histogram(drug_counts):
    counts = list(drug_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.hist(counts, bins=range(1, max(counts) + 2), edgecolor='black', align='left')
    plt.xlabel("Number of Pathways per Drug")
    plt.ylabel("Number of Drugs")
    plt.title("Pathways per Drug")
    plt.xticks(range(1, max(counts) + 1))
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Set the path to the DrugBank XML file.
    file_path = '../drugbank_partial.xml'
    
    # Optional: Uncomment to use the extended XML file.
    # file_path = '../drugbank_partial_and_generated.xml'

    # Parse the pathways from the XML.
    pathways = parse_all_pathways(file_path)
    
    # Build and print drug to pathway count mapping.
    drug_counts = build_drug_pathway_counts(pathways)
    print("Drug: pathway count:")
    for drug, count in sorted(drug_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{drug}: {count}")
    
    # Plot the histogram.
    display_histogram(drug_counts)
