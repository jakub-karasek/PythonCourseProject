import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_05 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_05"))
from subtask_05 import parse_all_pathways, display_graph

@pytest.fixture
def sample_xml(tmp_path):
    # Create a sample XML with two pathways.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug>
            <pathways>
              <pathway>
                <smpdb-id>SP0001</smpdb-id>
                <name>Pathway 1</name>
                <category>Cat1</category>
                <drugs>
                  <drug>
                    <drugbank-id>DB001</drugbank-id>
                    <name>Drug1</name>
                  </drug>
                  <drug>
                    <drugbank-id>DB002</drugbank-id>
                    <name>Drug2</name>
                  </drug>
                </drugs>
              </pathway>
              <pathway>
                <smpdb-id>SP0002</smpdb-id>
                <name>Pathway 2</name>
                <category>Cat2</category>
                <drugs>
                  <drug>
                    <drugbank-id>DB003</drugbank-id>
                    <name>Drug3</name>
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

def test_parse_all_pathways(sample_xml):
    # Parse the sample XML file.
    pathways_list = parse_all_pathways(str(sample_xml))
    
    # Verify that the returned value is a list and has 2 entries.
    assert isinstance(pathways_list, list)
    assert len(pathways_list) == 2
    
    # Verify the first pathway details.
    pathway1 = pathways_list[0]
    assert pathway1["id"] == "SP0001"
    assert pathway1["pathway_name"] == "Pathway 1"
    assert pathway1["category"] == "Cat1"
    # Check that drug lists are correct.
    assert pathway1["drug_ids"] == ["DB001", "DB002"]
    assert pathway1["drug_names"] == ["Drug1", "Drug2"]
    
    # Verify the second pathway details.
    pathway2 = pathways_list[1]
    assert pathway2["id"] == "SP0002"
    assert pathway2["pathway_name"] == "Pathway 2"
    assert pathway2["category"] == "Cat2"
    assert pathway2["drug_ids"] == ["DB003"]
    assert pathway2["drug_names"] == ["Drug3"]

def test_display_graph(sample_xml, monkeypatch):
    # Override plt.show to prevent the graph from actually displaying during tests.
    monkeypatch.setattr(plt, "show", lambda: None)
    
    # Parse sample XML and create DataFrame.
    pathways_list = parse_all_pathways(str(sample_xml))
    df = pd.DataFrame(pathways_list)
    
    # Call display_graph and ensure no exceptions are raised.
    try:
        display_graph(df)
    except Exception as e:
        pytest.fail(f"display_graph() raised an exception: {e}")