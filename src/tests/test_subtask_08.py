import os
import sys
import textwrap
import pytest
import pandas as pd
import matplotlib.pyplot as plt

# Add the subtask_08 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_08"))
from subtask_08 import parse_targets_info, create_donut_chart

@pytest.fixture
def sample_xml(tmp_path):
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <drugbank xmlns="http://www.drugbank.ca">
            <targets>
                <target>
                    <polypeptide>
                        <cellular-location>Membrane</cellular-location>
                    </polypeptide>
                </target>
                <target>
                    <!-- This target is missing polypeptide and should be skipped -->
                </target>
                <target>
                    <polypeptide>
                        <cellular-location> Cytoplasm </cellular-location>
                    </polypeptide>
                </target>
            </targets>
        </drugbank>
    """)
    xml_file = tmp_path / "sample_drugbank.xml"
    xml_file.write_text(xml_content)
    return xml_file

def test_parse_targets_info(sample_xml):
    df = parse_targets_info(str(sample_xml))
    
    # We expect only the two targets with a polypeptide.
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    
    # Check that the Cellular_location is trimmed correctly.
    expected_locations = ["Membrane", "Cytoplasm"]
    assert list(df["Cellular_location"]) == expected_locations

def test_create_donut_chart(monkeypatch):
    # Sample data for the donut chart.
    labels = ["Membrane", "Cytoplasm", "Other"]
    values = [10, 5, 3]
    title = "Test Donut Chart"
    
    # Override plt.show to prevent the chart from displaying.
    monkeypatch.setattr(plt, "show", lambda: None)
    
    # The function should run without errors.
    try:
        create_donut_chart(labels, values, title)
    except Exception as e:
        pytest.fail(f"create_donut_chart() raised an exception: {e}")