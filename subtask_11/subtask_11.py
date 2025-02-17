import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Return stripped text from a subelement.
def get_text(elem, tag, ns={'db': 'http://www.drugbank.ca'}):
    subelem = elem.find(tag, ns)
    return subelem.text.strip() if subelem is not None and subelem.text else None

# Parse XML to extract drugs for a target gene.
def parse_drugbank_for_gene(xml_file, target_gene):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    drugs_info = {}
    for drug in root.findall("db:drug", ns):
        targets_elem = drug.find("db:targets", ns)
        if targets_elem is None:
            continue
        gene_found = False
        for target in targets_elem.findall("db:target", ns):
            polypep = target.find("db:polypeptide", ns)
            if polypep is None:
                continue
            gene_name = get_text(polypep, "db:gene-name", ns)
            if gene_name and gene_name.lower() == target_gene.lower():
                gene_found = True
                break
        if not gene_found:
            continue
        primary_id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        if primary_id_elem is None or not primary_id_elem.text:
            continue
        drugbank_id = primary_id_elem.text.strip()
        drug_name = get_text(drug, "db:name", ns)
        
        products = []
        products_elem = drug.find("db:products", ns)
        if products_elem is not None:
            for product in products_elem.findall("db:product", ns):
                prod_name = get_text(product, "db:name", ns)
                if prod_name:
                    products.append(prod_name)
                    
        drugs_info[drugbank_id] = {
            "drug_name": drug_name,
            "products": products
        }
    
    return (target_gene, drugs_info)

# Plot gene-drug-product network from DataFrame.
def plot_gene_network(df, gene):
    G = nx.Graph()
    G.add_node(gene, type='gene')
    for idx, row in df.iterrows():
        drug = row['Drug_Name']
        G.add_node(drug, type='drug')
        G.add_edge(gene, drug)
        products_raw = [p.strip() for p in row['Products'].split(",") if p.strip()]
        unique_products = {p for p in products_raw if p.lower() != drug.lower()}
        for product in unique_products:
            G.add_node(product, type='product')
            G.add_edge(drug, product)
    pos = nx.spring_layout(G, seed=50, k=0.5)
    node_colors = []
    for node, attr in G.nodes(data=True):
        if attr.get('type') == 'gene':
            node_colors.append('tomato')
        elif attr.get('type') == 'drug':
            node_colors.append('lightblue')
        elif attr.get('type') == 'product':
            node_colors.append('lightgreen')
        else:
            node_colors.append('gray')
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200, font_size=10, edge_color='gray')
    plt.title(f'Gene-Drug-Product Network for gene: {gene}')
    plt.show()

if __name__ == "__main__":
    xml_file = '../drugbank_partial.xml'
    # Optional: Uncomment to use extended DrugBank XML file.
    # xml_file = '../drugbank_partial_and_generated.xml'
    
    target_gene = input("Enter gene name: ")
    gene, drugs = parse_drugbank_for_gene(xml_file, target_gene)
    
    rows = []
    for drugbank_id, info in drugs.items():
        rows.append({
            "Gene": gene,
            "DrugBank_ID": drugbank_id,
            "Drug_Name": info["drug_name"],
            "Products": ", ".join(info["products"]) if info["products"] else ""
        })
    df = pd.DataFrame(rows, columns=["Gene", "DrugBank_ID", "Drug_Name", "Products"])
    
    print(df)
    df.to_csv("drugbank_gene_interactions.csv", index=False)
    
    plot_gene_network(df, gene)
