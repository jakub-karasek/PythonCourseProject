import os
import sys
import textwrap
import pytest
import pandas as pd

# Add the subtask_01 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_01"))
from subtask_01 import parse_drugbank_xml

@pytest.fixture
def sample_xml(tmp_path):
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug type="small molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <name>Aspirin</name>
            <description>Used for pain relief.</description>
            <state>approved</state>
            <indication>Headache</indication>
            <mechanism-of-action>Inhibition of COX enzymes</mechanism-of-action>
            <food-interactions>None</food-interactions>
          </drug>
          <drug type="biotech">
            <drugbank-id primary="true">DB0002</drugbank-id>
            <name>Insulin</name>
            <description>Regulates blood sugar.</description>
            <state>approved</state>
            <indication>Diabetes</indication>
            <mechanism-of-action>Enables cellular uptake of glucose</mechanism-of-action>
            <food-interactions>Monitor carbohydrate intake</food-interactions>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_drugbank_xml(sample_xml):
    df = parse_drugbank_xml(str(sample_xml))
    
    # Check that the dataframe is not empty and has two records.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    
    # Test first record
    row1 = df.iloc[0]
    assert row1['drug_id'] == "DB0001"
    assert row1['name'] == "Aspirin"
    assert row1['type'] == "small molecule"
    assert row1['description'] == "Used for pain relief."
    assert row1['state'] == "approved"
    assert row1['indications'] == "Headache"
    assert row1['mechanism'] == "Inhibition of COX enzymes"
    assert row1['food_interactions'] == "None"
    
    # Test second record
    row2 = df.iloc[1]
    assert row2['drug_id'] == "DB0002"
    assert row2['name'] == "Insulin"
    assert row2['type'] == "biotech"
    assert row2['description'] == "Regulates blood sugar."
    assert row2['state'] == "approved"
    assert row2['indications'] == "Diabetes"
    assert row2['mechanism'] == "Enables cellular uptake of glucose"
    assert row2['food_interactions'] == "Monitor carbohydrate intake"