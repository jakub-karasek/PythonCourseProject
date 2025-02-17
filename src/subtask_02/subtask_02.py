import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Parse DrugBank XML and return a DataFrame.
def parse_drugbank_xml(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    drugs = []

    # Loop over each drug element.
    for drug in root.findall("db:drug", ns):
        # Drug identifier.
        id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        drug_id = id_elem.text if id_elem is not None else None

        # Drug name.
        name_elem = drug.find("db:name", ns)
        name = name_elem.text if name_elem is not None else None

        # Drug synonyms.
        synonyms = [elem.text for elem in drug.findall("db:synonyms/db:synonym", ns)]

        drugs.append({
            "drug_id": drug_id,
            "name": name,
            "synonyms": synonyms
        })

    return pd.DataFrame(drugs)

# Create and display a synonyms graph.
def display_synonym_graph(drugbank_id, df):
    # Find drug record by DrugBank ID.
    drug_record = df[df['drug_id'] == drugbank_id]
    if drug_record.empty:
        print(f"No drug found with DrugBank ID: {drugbank_id}")
        return

    drug_name = drug_record.iloc[0]['name']
    synonyms = drug_record.iloc[0]['synonyms']

    # Create a graph.
    G = nx.Graph()
    G.add_node(drug_name)  # Central node.

    # Add nodes and edges for synonyms.
    for synonym in synonyms:
        if synonym and synonym != drug_name:
            G.add_node(synonym)
            G.add_edge(drug_name, synonym)

    # Plot the graph.
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, k=0.15, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1700)
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.title(f"Synonyms Graph for {drugbank_id} ({drug_name})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Path to the DrugBank XML file.
    file_path = '../drugbank_partial.xml'
    
    # Optional: Uncomment to use the extended XML file.
    # file_path = '../drugbank_partial_and_generated.xml'

    df = parse_drugbank_xml(file_path)
    print(df)
    # Save the DataFrame to a CSV file.
    df.to_csv('drugbank_drugs.csv', index=False)

    # Prompt user for a DrugBank ID and display its graph.
    drugbank_id_input = input("Enter DrugBank ID: ").strip()
    display_synonym_graph(drugbank_id_input, df)
