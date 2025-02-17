import os
import sys
import copy
import random
import textwrap
import pytest
import xml.etree.ElementTree as ET

# Add the subtask_13 directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subtask_13"))
from subtask_13 import get_namespace, strip_ns, build_pools, create_new_drug

@pytest.fixture
def sample_drug_xml():
    # Sample XML with 2 drug elements using the DrugBank namespace.
    xml_content = textwrap.dedent("""\
        <?xml version="1.0"?>
        <db:drugbank xmlns:db="http://www.drugbank.ca">
          <db:drug type="small molecule">
            <db:drugbank-id primary="true">DB0001</db:drugbank-id>
            <db:name>DrugOne</db:name>
            <db:description>Description One</db:description>
          </db:drug>
          <db:drug type="small molecule">
            <db:drugbank-id primary="true">DB0002</db:drugbank-id>
            <db:name>DrugTwo</db:name>
            <db:description>Description Two</db:description>
          </db:drug>
        </db:drugbank>
    """)
    return xml_content

@pytest.fixture
def parsed_drugs(sample_drug_xml):
    tree = ET.ElementTree(ET.fromstring(sample_drug_xml))
    root = tree.getroot()
    ns_uri = get_namespace(root)
    ns = {"db": ns_uri}
    # Find all <drug> elements using the namespace
    drugs = root.findall("db:drug", ns)
    return drugs, ns_uri

def test_build_pools(parsed_drugs):
    drugs, ns_uri = parsed_drugs
    # build_pools should collect child elements of each drug (skipping the drugbank-id).
    pools = build_pools(drugs)
    # In our sample each drug has children: drugbank-id, name, description.
    # The function should skip the "drugbank-id" tag.
    assert "name" in pools
    assert "description" in pools
    # For 2 drugs, there should be 2 elements in each pool.
    assert len(pools["name"]) == 2
    assert len(pools["description"]) == 2

def test_create_new_drug(parsed_drugs, monkeypatch):
    drugs, ns_uri = parsed_drugs
    pools = build_pools(drugs)
    original_attribs = {}
    new_id = 3
    # Force random.choice to always select the first element for predictability.
    monkeypatch.setattr(random, "choice", lambda lst: lst[0])
    new_drug = create_new_drug(new_id, pools, ns_uri, original_attribs)
    
    # Instead of using ET.QName().localname, we manually extract the local name.
    localname = new_drug.tag.split("}")[-1] if "}" in new_drug.tag else new_drug.tag
    assert localname == "drug"
    
    # Verify the generated drugbank-id
    drugbank_id_elem = new_drug.find(f"{{{ns_uri}}}drugbank-id")
    assert drugbank_id_elem is not None
    expected_id = f"DB{new_id:05d}"  # Format: DB00003 for new_id = 3
    assert drugbank_id_elem.text == expected_id
    
    # The new drug should include one element for each pool (plus the newly added drugbank-id).
    num_expected_children = 1 + len(pools)
    assert len(new_drug) == num_expected_children