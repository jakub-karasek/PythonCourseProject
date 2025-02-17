import os
import sys
import textwrap
import pytest
import pandas as pd

# Add the subtask_03 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_03"))
from subtask_03 import parse_pharma_products

@pytest.fixture
def sample_xml(tmp_path):
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug type="small molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <products>
              <product>
                <name>Aspirin Tablet</name>
                <labeller>Bayer</labeller>
                <ndc-product-code>12345</ndc-product-code>
                <dosage-form>Tablet</dosage-form>
                <route>Oral</route>
                <strength>500 mg</strength>
                <fda-application-number>FDA123</fda-application-number>
              </product>
              <product>
                <name>Aspirin Capsule</name>
                <labeller>Bayer</labeller>
                <ndc-product-code>67890</ndc-product-code>
                <dosage-form>Capsule</dosage-form>
                <route>Oral</route>
                <strength>250 mg</strength>
                <ema-product-code>EMA456</ema-product-code>
              </product>
            </products>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_pharma_products(sample_xml):
    df = parse_pharma_products(str(sample_xml))
    
    # Verify that the resulting DataFrame has two rows.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2

    # Test first product (with FDA application number)
    prod1 = df.iloc[0]
    assert prod1['drug_id'] == "DB0001"
    assert prod1['product_name'] == "Aspirin Tablet"
    assert prod1['producer'] == "Bayer"
    assert prod1['ndc_product_code'] == "12345"
    assert prod1['dosage_form'] == "Tablet"
    assert prod1['route'] == "Oral"
    assert prod1['strength'] == "500 mg"
    assert prod1['country'] == "USA"        # Because fda-application-number is present
    assert prod1['regulatory_agency'] == "FDA"
    
    # Test second product (with EMA product code)
    prod2 = df.iloc[1]
    assert prod2['drug_id'] == "DB0001"
    assert prod2['product_name'] == "Aspirin Capsule"
    assert prod2['producer'] == "Bayer"
    assert prod2['ndc_product_code'] == "67890"
    assert prod2['dosage_form'] == "Capsule"
    assert prod2['route'] == "Oral"
    assert prod2['strength'] == "250 mg"
    assert prod2['country'] == "EU"         # Because ema-product-code is present
    assert prod2['regulatory_agency'] == "EMA"