import os
import sys
import textwrap
import pytest
import pandas as pd
import xml.etree.ElementTree as ET

# Add the subtask_12 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_12"))
from subtask_12 import parse_drugbank_xml, fetch_uniprot_details

@pytest.fixture
def sample_drugbank_xml(tmp_path):
    # Updated sample XML with proper namespace prefixes so that the parser finds the elements.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <db:drugbank xmlns:db="http://www.drugbank.ca">
          <db:drug type="small molecule">
            <db:drugbank-id primary="true">DB0001</db:drugbank-id>
            <db:name>Test Drug</db:name>
            <db:description>Test description</db:description>
            <db:state>approved</db:state>
            <db:indication>Test indication</db:indication>
            <db:mechanism-of-action>Test mechanism</db:mechanism-of-action>
            <db:food-interactions>None</db:food-interactions>
            <db:targets>
              <db:target>
                <db:polypeptide>
                  <db:external-identifiers>
                    <db:external-identifier>
                      <db:resource>UniProtKB</db:resource>
                      <db:identifier>P12345</db:identifier>
                    </db:external-identifier>
                  </db:external-identifiers>
                </db:polypeptide>
              </db:target>
            </db:targets>
          </db:drug>
        </db:drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_drugbank_xml(sample_drugbank_xml):
    df = parse_drugbank_xml(str(sample_drugbank_xml))
    
    # Verify that the DataFrame contains one record with the expected values.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    
    row = df.iloc[0]
    assert row['drug_id'] == "DB0001"
    assert row['name'] == "Test Drug"
    assert row['description'] == "Test description"
    assert row['state'] == "approved"
    # Check that the uniprot_id is correctly extracted.
    assert row['uniprot_id'] == "P12345"

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

def dummy_requests_get(url, headers, timeout):
    # Provide dummy UniProt XML response.
    dummy_uniprot_xml = textwrap.dedent("""\
        <?xml version="1.0"?>
        <up:uniprot xmlns:up="http://uniprot.org/uniprot">
          <up:entry>
            <up:comment type="function">
              <up:text>This protein functions as a test.</up:text>
            </up:comment>
            <up:comment type="subcellular location">
              <up:text>Test Location</up:text>
            </up:comment>
          </up:entry>
        </up:uniprot>
    """)
    return DummyResponse(dummy_uniprot_xml, status_code=200)

def test_fetch_uniprot_details(monkeypatch):
    # Override requests.get in fetch_uniprot_details to use our dummy response.
    monkeypatch.setattr("subtask_12.requests.get", dummy_requests_get)
    
    uniprot_id = "P12345"
    details = fetch_uniprot_details(uniprot_id)
    
    # Check that the returned details dictionary contains the dummy data.
    assert isinstance(details, dict)
    assert details.get("function") == "This protein functions as a test."
    assert details.get("subcellular_location") == "Test Location"
    
    # Clean up the file that might have been created.
    xml_filename = "uniprot_drug_data.xml"
    if os.path.exists(xml_filename):
        os.remove(xml_filename)