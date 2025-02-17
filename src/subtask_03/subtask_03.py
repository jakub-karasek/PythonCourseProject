import xml.etree.ElementTree as ET
import pandas as pd

# Parse DrugBank XML and return a DataFrame of pharma products.
def parse_pharma_products(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    products_list = []

    # Loop over each drug element.
    for drug in root.findall("db:drug", ns):
        # Get primary DrugBank ID.
        id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        drug_id = id_elem.text if id_elem is not None else None

        # Parse products for the drug.
        products = drug.find("db:products", ns)
        if products is not None:
            for prod in products.findall("db:product", ns):
                # Get product name.
                prod_name_elem = prod.find("db:name", ns)
                product_name = prod_name_elem.text if prod_name_elem is not None else None

                # Get producer.
                labeller_elem = prod.find("db:labeller", ns)
                producer = labeller_elem.text if labeller_elem is not None else None

                # Get NDC product code.
                ndc_elem = prod.find("db:ndc-product-code", ns)
                ndc = ndc_elem.text if ndc_elem is not None else None

                # Get dosage form.
                dosage_elem = prod.find("db:dosage-form", ns)
                dosage_form = dosage_elem.text if dosage_elem is not None else None

                # Get route of administration.
                route_elem = prod.find("db:route", ns)
                route = route_elem.text if route_elem is not None else None

                # Get strength.
                strength_elem = prod.find("db:strength", ns)
                strength = strength_elem.text if strength_elem is not None else None

                # Determine regulatory agency based on available codes.
                fda_elem = prod.find("db:fda-application-number", ns)
                ema_elem = prod.find("db:ema-product-code", ns)

                if fda_elem is not None and fda_elem.text and fda_elem.text.strip() != "":
                    country = "USA"
                    agency = "FDA"
                elif ema_elem is not None and ema_elem.text and ema_elem.text.strip() != "":
                    country = "EU"
                    agency = "EMA"
                else:
                    country = None
                    agency = None

                products_list.append({
                    "drug_id": drug_id,
                    "product_name": product_name,
                    "producer": producer,
                    "ndc_product_code": ndc,
                    "dosage_form": dosage_form,
                    "route": route,
                    "strength": strength,
                    "country": country,
                    "regulatory_agency": agency
                })

    return pd.DataFrame(products_list)

if __name__ == '__main__':
    # Path to the DrugBank XML file.
    file_path = '../drugbank_partial.xml'
    # Optional: Uncomment to use the extended XML file.
    # file_path = '../drugbank_partial_and_generated.xml'

    # Parse and display pharma product data.
    df_products = parse_pharma_products(file_path)
    print(df_products)

    # Optionally, save the DataFrame to a CSV file.
    df_products.to_csv('pharma_products.csv', index=False)