import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_09 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_09"))
from subtask_09 import parse_drug_status, create_donut_chart

@pytest.fixture
def sample_xml(tmp_path):
    # This sample XML contains 4 drug entries:
    # Drug 1: groups: Approved, Experimental
    # Drug 2: groups: Withdrawn, Vet_Approved
    # Drug 3: groups: Approved
    # Drug 4: no groups element, so all flags should be False.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
            <drug>
                <groups>
                    <group>Approved</group>
                    <group>Experimental</group>
                </groups>
            </drug>
            <drug>
                <groups>
                    <group>Withdrawn</group>
                    <group>Vet_Approved</group>
                </groups>
            </drug>
            <drug>
                <groups>
                    <group>Approved</group>
                </groups>
            </drug>
            <drug>
                <!-- No groups element -->
                <name>Test Drug</name>
            </drug>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_drug_status(sample_xml):
    df = parse_drug_status(str(sample_xml))
    
    # Verify that the DataFrame is created with 4 records.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    
    # Expected values:
    # Row 0: approved: True, withdrawn: False, experimental: True, vet_approved: False
    # Row 1: approved: False, withdrawn: True, experimental: False, vet_approved: True
    # Row 2: approved: True, withdrawn: False, experimental: False, vet_approved: False
    # Row 3: all False.
    
    row0 = df.iloc[0]
    assert row0['approved'] == True
    assert row0['withdrawn'] == False
    assert row0['experimental'] == True
    assert row0['vet_approved'] == False

    row1 = df.iloc[1]
    assert row1['approved'] == False
    assert row1['withdrawn'] == True
    assert row1['experimental'] == False
    assert row1['vet_approved'] == True

    row2 = df.iloc[2]
    assert row2['approved'] == True
    assert row2['withdrawn'] == False
    assert row2['experimental'] == False
    assert row2['vet_approved'] == False

    row3 = df.iloc[3]
    assert row3['approved'] == False
    assert row3['withdrawn'] == False
    assert row3['experimental'] == False
    assert row3['vet_approved'] == False

def test_create_donut_chart(monkeypatch):
    # Prepare sample status counts and labels that mimic the output of the main script.
    labels = ["Approved", "Withdrawn", "Experimental/Investigational", "Vet Approved"]
    counts = [2, 1, 1, 1]
    title = "Drug Status Distribution (Sorted Ascending by Percentage)"
    
    # Override plt.show to prevent the chart from displaying during the test.
    monkeypatch.setattr(plt, "show", lambda: None)

    # The function should execute without errors.
    try:
        create_donut_chart(labels, counts, title)
    except Exception as e:
        pytest.fail(f"create_donut_chart() raised an exception: {e}")