import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_06 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_06"))
from subtask_06 import parse_all_pathways, build_drug_pathway_counts, display_histogram

@pytest.fixture
def sample_xml(tmp_path):
    # This sample XML contains 2 pathways:
    #   - Pathway "P1" with drugs: "DrugA" and "DrugB"
    #   - Pathway "P2" with drugs: "DrugA" and "DrugC"
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug>
            <pathways>
              <pathway>
                <smpdb-id>P001</smpdb-id>
                <name>P1</name>
                <category>Cat1</category>
                <drugs>
                  <drug>
                    <drugbank-id>DB01</drugbank-id>
                    <name>DrugA</name>
                  </drug>
                  <drug>
                    <drugbank-id>DB02</drugbank-id>
                    <name>DrugB</name>
                  </drug>
                </drugs>
              </pathway>
              <pathway>
                <smpdb-id>P002</smpdb-id>
                <name>P2</name>
                <category>Cat2</category>
                <drugs>
                  <drug>
                    <drugbank-id>DB01</drugbank-id>
                    <name>DrugA</name>
                  </drug>
                  <drug>
                    <drugbank-id>DB03</drugbank-id>
                    <name>DrugC</name>
                  </drug>
                </drugs>
              </pathway>
            </pathways>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_build_drug_pathway_counts(sample_xml):
    # Parse the XML to get pathways list.
    pathways = parse_all_pathways(str(sample_xml))
    
    # Build the drug to pathway count mapping.
    drug_counts = build_drug_pathway_counts(pathways)
    
    # Expected outcome:
    # DrugA appears in pathways "P1" and "P2" => count 2
    # DrugB appears only in "P1" => count 1
    # DrugC appears only in "P2" => count 1
    expected = {
        "DrugA": 2,
        "DrugB": 1,
        "DrugC": 1
    }
    assert drug_counts == expected

def test_display_histogram(monkeypatch):
    # Create a sample drug_counts dictionary.
    sample_counts = {"DrugA": 2, "DrugB": 1, "DrugC": 1}
    
    # Override plt.show to avoid opening a window during tests.
    monkeypatch.setattr(plt, "show", lambda: None)
    
    # Calling display_histogram should run without error.
    try:
        display_histogram(sample_counts)
    except Exception as e:
        pytest.fail(f"display_histogram() raised an exception: {e}")