import os
import sys
import textwrap
import pytest
import pandas as pd

# Add the subtask_04 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_04"))
from subtask_04 import parse_all_pathways

@pytest.fixture
def sample_xml(tmp_path):
    # Create a sample XML containing two drugs with a total of 3 pathways.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug>
            <pathways>
              <pathway>
                <smpdb-id>SP0001</smpdb-id>
                <name>Metabolic Pathway</name>
                <category>Metabolism</category>
              </pathway>
              <pathway>
                <smpdb-id>SP0002</smpdb-id>
                <name>Signal Transduction</name>
                <category>Signaling</category>
              </pathway>
            </pathways>
          </drug>
          <drug>
            <pathways>
              <pathway>
                <smpdb-id>SP0003</smpdb-id>
                <name>Cell Cycle</name>
                <category>Cellular Process</category>
              </pathway>
            </pathways>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_all_pathways(sample_xml):
    # Parse the sample XML file
    pathways_list = parse_all_pathways(str(sample_xml))
    
    # Check that the returned value is a list with 3 pathway entries.
    assert isinstance(pathways_list, list)
    assert len(pathways_list) == 3
    
    # Create a DataFrame for easier inspection (optional)
    df = pd.DataFrame(pathways_list)
    # Check that required keys are present in each entry
    expected_keys = {"id", "pathway_name", "category"}
    for pathway in pathways_list:
        assert expected_keys.issubset(pathway.keys())
    
    # Verify content for the first pathway
    pathway1 = pathways_list[0]
    assert pathway1["id"] == "SP0001"
    assert pathway1["pathway_name"] == "Metabolic Pathway"
    assert pathway1["category"] == "Metabolism"

    # Verify content for the second pathway
    pathway2 = pathways_list[1]
    assert pathway2["id"] == "SP0002"
    assert pathway2["pathway_name"] == "Signal Transduction"
    assert pathway2["category"] == "Signaling"

    # Verify content for the third pathway
    pathway3 = pathways_list[2]
    assert pathway3["id"] == "SP0003"
    assert pathway3["pathway_name"] == "Cell Cycle"
    assert pathway3["category"] == "Cellular Process"