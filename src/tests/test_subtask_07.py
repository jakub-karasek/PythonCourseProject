import os
import sys
import textwrap
import pytest
import pandas as pd

# Add the subtask_07 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_07"))
from subtask_07 import parse_targets_info

@pytest.fixture
def sample_xml(tmp_path):
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <targets>
            <target>
              <id>DBT001</id>
              <polypeptide id="P001" source="SwissProt">
                <name>PolyA</name>
                <gene-name>GENE1</gene-name>
                <chromosome-location>1p36</chromosome-location>
                <cellular-location>Cytoplasm</cellular-location>
                <external-identifiers>
                  <external-identifier>
                    <resource>GenAtlas</resource>
                    <identifier>GA001</identifier>
                  </external-identifier>
                </external-identifiers>
              </polypeptide>
            </target>
            <!-- This target does not have a polypeptide and should be skipped -->
            <target>
              <id>DBT002</id>
            </target>
          </targets>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_targets_info(sample_xml):
    df = parse_targets_info(str(sample_xml))
    
    # We expect only one target record since the second target (without polypeptide) is skipped.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    
    # Check that the DataFrame has the expected columns
    expected_columns = {
        "DrugBank_ID", "Source", "External_ID", "Polypeptide_name",
        "Gene_name", "GenAtlas_ID", "Chromosome", "Cellular_location"
    }
    assert expected_columns.issubset(set(df.columns))
    
    # Verify the content of the first (and only) record
    row = df.iloc[0]
    assert row["DrugBank_ID"] == "DBT001"
    assert row["Source"] == "SwissProt"
    assert row["External_ID"] == "P001"
    assert row["Polypeptide_name"] == "PolyA"
    assert row["Gene_name"] == "GENE1"
    assert row["GenAtlas_ID"] == "GA001"
    assert row["Chromosome"] == "1p36"
    assert row["Cellular_location"] == "Cytoplasm"