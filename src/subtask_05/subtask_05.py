import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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
                category_elem = pathway.find("db:category", ns)
                pathway_category = category_elem.text if category_elem is not None else None

                # Parse drug IDs and names in the pathway.
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

# Display a bipartite graph of pathways and drugs.
def display_graph(df):
    B = nx.Graph()
    # Add pathway nodes.
    pathway_nodes = set(df['pathway_name'].tolist())
    for p in pathway_nodes:
        if p:
            B.add_node(p, bipartite=0)

    # Add drug nodes and connect them to pathways.
    drug_nodes = set()
    for _, row in df.iterrows():
        p_name = row['pathway_name']
        for drug in row['drug_names']:
            if drug:
                drug_nodes.add(drug)
                B.add_node(drug, bipartite=1)
                B.add_edge(p_name, drug)

    # Create bipartite layout.
    pos = nx.bipartite_layout(B, pathway_nodes)

    plt.figure(figsize=(14, 8))
    nx.draw_networkx_nodes(B, pos, nodelist=list(pathway_nodes), node_color='lightblue', node_size=1000, label='Pathways')
    nx.draw_networkx_nodes(B, pos, nodelist=list(drug_nodes), node_color='lightgreen', node_size=900, label='Drugs')
    nx.draw_networkx_edges(B, pos, edge_color='gray')
    nx.draw_networkx_labels(B, pos, font_size=11, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    plt.title("Bipartite Graph of Pathways and Drugs", fontsize=14)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.06), markerscale=0.5, ncol=2)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Path to DrugBank XML file.
    file_path = '../drugbank_partial.xml'
    # Optional: Uncomment to use the extended XML file.
    file_path = '../drugbank_partial_and_generated.xml'

    pathways = parse_all_pathways(file_path)
    df_pathways = pd.DataFrame(pathways)

    print(df_pathways)
    # Display total number of pathways.
    print(f"\nTotal number of pathways: {len(df_pathways)}")

    # Show the bipartite graph.
    display_graph(df_pathways)
