import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_02 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_02"))
from subtask_02 import parse_drugbank_xml, display_synonym_graph

@pytest.fixture
def sample_xml(tmp_path):
    # Create a sample XML with synonyms for testing.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug type="small molecule">
            <drugbank-id primary="true">DB0001</drugbank-id>
            <name>Aspirin</name>
            <synonyms>
                <synonym>Acetylsalicylic Acid</synonym>
                <synonym>ASA</synonym>
            </synonyms>
          </drug>
          <drug type="biotech">
            <drugbank-id primary="true">DB0002</drugbank-id>
            <name>Insulin</name>
            <synonyms>
                <synonym>Humulin</synonym>
            </synonyms>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_display_synonym_graph_valid(sample_xml, monkeypatch):
    # Prevent plt.show() from actually displaying a window during the test.
    monkeypatch.setattr(plt, "show", lambda: None)
    
    # Parse the sample XML to create the dataframe.
    df = parse_drugbank_xml(str(sample_xml))
    
    # Use an existing DrugBank ID.
    valid_id = "DB0001"
    
    # Calling the display_synonym_graph should complete without error.
    try:
        display_synonym_graph(valid_id, df)
    except Exception as e:
        pytest.fail(f"display_synonym_graph() raised an exception for valid input: {e}")

def test_display_synonym_graph_invalid(sample_xml, capsys):
    # Parse the sample XML to create the dataframe.
    df = parse_drugbank_xml(str(sample_xml))
    
    # Use an invalid DrugBank ID.
    invalid_id = "DB9999"
    
    # Capture printed output.
    display_synonym_graph(invalid_id, df)
    captured = capsys.readouterr().out.strip()
    expected = f"No drug found with DrugBank ID: {invalid_id}"
    assert expected in captured