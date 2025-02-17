import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_11 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_11"))
from subtask_11 import parse_drugbank_for_gene, plot_gene_network

@pytest.fixture
def sample_xml(tmp_path):
    # Sample XML with two drugs:
    # - The first drug targets gene "BRCA1" and has two products:
    #   one product with a different name and one identical to the drug name (should be ignored).
    # - The second drug targets gene "BRCA2" (won't be returned when searching for BRCA1).
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
          <drug>
            <drugbank-id primary="true">DB001</drugbank-id>
            <name>DrugOne</name>
            <targets>
              <target>
                <polypeptide>
                  <gene-name>BRCA1</gene-name>
                </polypeptide>
              </target>
            </targets>
            <products>
              <product>
                <name>ProductA</name>
              </product>
              <product>
                <name>DrugOne</name>
              </product>
            </products>
          </drug>
          <drug>
            <drugbank-id primary="true">DB002</drugbank-id>
            <name>DrugTwo</name>
            <targets>
              <target>
                <polypeptide>
                  <gene-name>BRCA2</gene-name>
                </polypeptide>
              </target>
            </targets>
            <products>
              <product>
                <name>ProductB</name>
              </product>
            </products>
          </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_drugbank_for_gene(sample_xml):
    # Search for gene "BRCA1". Expect only the first drug to be returned.
    target_gene = "BRCA1"
    gene, drugs_info = parse_drugbank_for_gene(str(sample_xml), target_gene)
    
    assert gene.lower() == target_gene.lower()
    # Only one drug (DB001) should be returned.
    assert isinstance(drugs_info, dict)
    assert len(drugs_info) == 1
    assert "DB001" in drugs_info
    
    drug_info = drugs_info["DB001"]
    assert drug_info["drug_name"] == "DrugOne"
    # The products list should contain 'ProductA' and 'DrugOne'
    # (ignoring filtering is done later in the network plot).
    assert isinstance(drug_info["products"], list)
    assert "ProductA" in drug_info["products"]
    assert "DrugOne" in drug_info["products"]

def test_plot_gene_network(monkeypatch):
    # Create a sample DataFrame mimicking the output from parse_drugbank_for_gene.
    data = {
        "Gene": ["BRCA1"],
        "DrugBank_ID": ["DB001"],
        "Drug_Name": ["DrugOne"],
        # Products string includes a product different from the drug name and one identical.
        "Products": ["ProductA, DrugOne"]
    }
    df = pd.DataFrame(data, columns=["Gene", "DrugBank_ID", "Drug_Name", "Products"])
    gene = "BRCA1"
    
    # Override plt.show to prevent actual display during testing.
    monkeypatch.setattr(plt, "show", lambda: None)
    
    try:
        plot_gene_network(df, gene)
    except Exception as e:
        pytest.fail(f"plot_gene_network() raised an exception: {e}")