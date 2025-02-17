import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parse DrugBank XML and create a DataFrame with drug status information.
def parse_drug_status(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    drugs_data = []
    for drug in root.findall('.//db:drug', ns):
        groups_elem = drug.find('db:groups', ns)
        if groups_elem is not None:
            groups = [grp.text.strip().lower() for grp in groups_elem.findall('db:group', ns) if grp.text]
        else:
            groups = []
        drugs_data.append({
            "approved": "approved" in groups,
            "withdrawn": "withdrawn" in groups,
            "experimental": ("experimental" in groups or "investigational" in groups),
            "vet_approved": "vet_approved" in groups
        })

    return pd.DataFrame(drugs_data)

# Create a donut chart with percentage labels and external annotations using arrows.
def create_donut_chart(labels, counts, title):
    fig, ax = plt.subplots(figsize=(14, 8), subplot_kw=dict(aspect="equal"))
    
    # Plot pie chart with autopct showing percentages.
    wedges, texts, autotexts = ax.pie(
        counts,
        autopct='%1d%%',
        pctdistance=0.85,
        wedgeprops=dict(width=0.5),
        startangle=-40
    )
    
    # Customize the percentage text appearance.
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(12)
    
    # Annotate external labels with arrows.
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        ax.annotate(
            labels[i],
            xy=(x, y),
            xytext=(1 * np.sign(x), 1.3 * y),
            horizontalalignment=horizontalalignment,
            bbox=bbox_props,
            arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle)
        )

    ax.set_title(title)
    plt.show()

if __name__ == "__main__":
    file_path = '../drugbank_partial.xml'
    
    # Optional: uncomment to use the extended DrugBank XML file.
    file_path = '../drugbank_partial_and_generated.xml'

    df = parse_drug_status(file_path)

    # Count drugs in each category.
    total_approved = df['approved'].sum()
    total_withdrawn = df['withdrawn'].sum()
    total_experimental = df['experimental'].sum()
    total_vet = df['vet_approved'].sum()
    approved_not_withdrawn = ((df['approved'] == True) & (df['withdrawn'] == False)).sum()

    # Create a DataFrame with the required counts.
    status_counts = {
        "Approved": total_approved,
        "Withdrawn": total_withdrawn,
        "Experimental/Investigational": total_experimental,
        "Vet Approved": total_vet
    }
    df_status = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
    
    # Sort the DataFrame by counts in ascending order.
    df_status = df_status.sort_values(by="Count", ascending=True)
    
    print(df_status)
    print("Approved but not withdrawn:", approved_not_withdrawn)

    # Prepare donut chart data and generate the chart.
    labels = list(df_status["Status"])
    counts = list(df_status["Count"])
    
    create_donut_chart(labels, counts, "Drug Status Distribution (Sorted Ascending by Percentage)")
