import os
import sys
import textwrap
import pytest
import pandas as pd

# Add the subtask_10 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_10"))
from subtask_10 import parse_drug_interactions

@pytest.fixture
def sample_xml(tmp_path):
    # Create a sample XML with two drugs.
    # Drug A (DB0001) interacts with Drug B (DB0002).
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug type="small molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <name>DrugA</name>
            <drug-interactions>
              <drug-interaction drugbank-id="DB0002" name="DrugB">
                <description>Interaction description between DrugA and DrugB</description>
              </drug-interaction>
            </drug-interactions>
          </drug>
          <drug type="biotech">
            <drugbank-id primary="true">DB0002</drugbank-id>
            <name>DrugB</name>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_drug_interactions(sample_xml):
    df = parse_drug_interactions(str(sample_xml))
    
    # We expect one interaction record.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    
    # Verify the content of the interaction record
    row = df.iloc[0]
    assert row["DrugBank_ID"] == "DB0001"
    assert row["Drug_Official_Name"] == "DrugA"
    assert row["Interacting_DrugBank_ID"] == "DB0002"
    assert row["Interacting_Drug_Name"] == "DrugB"
    assert row["Description"] == "Interaction description between DrugA and DrugB"