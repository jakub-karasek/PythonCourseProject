import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parse DrugBank XML and return a DataFrame with cellular location information for targets.
def parse_targets_info(file_path):
    ns = {'db': 'http://www.drugbank.ca'}
    tree = ET.parse(file_path)
    root = tree.getroot()

    targets_data = []
    for target in root.findall('.//db:target', ns):
        polypep = target.find('db:polypeptide', ns)
        if polypep is None:
            continue

        cell_loc_elem = polypep.find('db:cellular-location', ns)
        cellular_location = cell_loc_elem.text.strip() if cell_loc_elem is not None and cell_loc_elem.text else None

        targets_data.append({
            "Cellular_location": cellular_location
        })

    return pd.DataFrame(targets_data)

# Create a donut (ring) chart with percentages and labels outside the chart connected by arrows.
def create_donut_chart(labels, values, title):
    fig, ax = plt.subplots(figsize=(14, 8), subplot_kw=dict(aspect="equal"))
    
    # Plot pie chart with autopct showing percentages.
    wedges, texts, autotexts = ax.pie(
        values,
        autopct='%1d%%',
        pctdistance=0.85,
        wedgeprops=dict(width=0.5),
        startangle=-40
    )
    
    # Customize percentage text.
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(12)
    
    # Annotate labels outside the donut with arrows.
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        ax.annotate(labels[i],
                    xy=(x, y),
                    xytext=(1.35 * np.sign(x), 1.7 * y),
                    horizontalalignment=horizontalalignment,
                    bbox=bbox_props,
                    arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))
    
    ax.set_title(title)
    plt.show()

if __name__ == "__main__":
    file_path = '../drugbank_partial.xml'
    # Optional: uncomment to use the extended DrugBank XML file.
    file_path = '../drugbank_partial_and_generated.xml'

    df = parse_targets_info(file_path)
    print(df)
    df.to_csv('targets_info.csv', index=False)

    # Prepare data for the donut chart: top 5 cellular locations, others grouped as "Other".
    location_counts = df['Cellular_location'].value_counts()
    top_n = 5
    top_locations = location_counts[:top_n]
    others = location_counts[top_n:].sum()

    labels = list(top_locations.index)
    values = list(top_locations.values)
    if others > 0:
        labels.append("Other")
        values.append(others)

    create_donut_chart(
        labels, values,
        "The percentage occurrence of targets in different parts of the cell"
    )
