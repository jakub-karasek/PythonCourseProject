import xml.etree.ElementTree as ET
import pandas as pd

# Parse DrugBank XML to create a DataFrame of targets information.
def parse_targets_info(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    targets_data = []
    # Loop over each target element.
    for target in root.findall(".//db:target", ns):
        # Get DrugBank target ID.
        target_id_elem = target.find("db:id", ns)
        drugbank_id = target_id_elem.text.strip() if target_id_elem is not None and target_id_elem.text else None

        # Get polypeptide element.
        polypep = target.find("db:polypeptide", ns)
        if polypep is None:
            continue

        # Get source and external ID.
        external_id = polypep.attrib.get("id")
        source = polypep.attrib.get("source")

        # Get polypeptide name.
        pep_name_elem = polypep.find("db:name", ns)
        polypeptide_name = pep_name_elem.text.strip() if pep_name_elem is not None and pep_name_elem.text else None

        # Get gene name.
        gene_name_elem = polypep.find("db:gene-name", ns)
        gene_name = gene_name_elem.text.strip() if gene_name_elem is not None and gene_name_elem.text else None

        # Get chromosome location.
        chrom_elem = polypep.find("db:chromosome-location", ns)
        chromosome = chrom_elem.text.strip() if chrom_elem is not None and chrom_elem.text else None

        # Get cellular location.
        cell_loc_elem = polypep.find("db:cellular-location", ns)
        cellular_location = cell_loc_elem.text.strip() if cell_loc_elem is not None and cell_loc_elem.text else None

        # Get GenAtlas ID.
        genatlas_id = None
        ext_ids_elem = polypep.find("db:external-identifiers", ns)
        if ext_ids_elem is not None:
            for ext in ext_ids_elem.findall("db:external-identifier", ns):
                resource_elem = ext.find("db:resource", ns)
                if resource_elem is not None and resource_elem.text.strip() == "GenAtlas":
                    identifier_elem = ext.find("db:identifier", ns)
                    if identifier_elem is not None and identifier_elem.text:
                        genatlas_id = identifier_elem.text.strip()
                        break

        targets_data.append({
            "DrugBank_ID": drugbank_id,
            "Source": source,
            "External_ID": external_id,
            "Polypeptide_name": polypeptide_name,
            "Gene_name": gene_name,
            "GenAtlas_ID": genatlas_id,
            "Chromosome": chromosome,
            "Cellular_location": cellular_location
        })

    return pd.DataFrame(targets_data)

if __name__ == "__main__":
    # Path to the DrugBank XML file.
    file_path = "../drugbank_partial.xml"
    # Optional: Uncomment to use the extended XML file.
    # file_path = "../drugbank_partial_and_generated.xml"

    df = parse_targets_info(file_path)
    print(df)

    # Optionally, save the DataFrame to a CSV file.
    df.to_csv("targets_info.csv", index=False)
