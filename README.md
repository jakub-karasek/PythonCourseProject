# PythonCourseProject
Python Course Project - Faculty of Mathematics, Informatics, and Mechanics, University of Warsaw

# Task description

The DrugBank database is a publicly accessible and free database of drug information (pharmaceutical substances). It was created in 2006 by the team of Craig Knox and David Wishart from the Faculty of Computing and Biological Sciences at the University of Alberta in Canada. It integrates data from the fields of chemistry, biochemistry, genetics, pharmacology, and pharmacokinetics.

Since access to the full database requires creating an account, filling out a form with a justification for the request, and obtaining approval, for the purpose of this assignment a file named drugbank_partial.xml with a reduced version of the database will be provided. This file contains data for 100 drugs (the full database published on 2024-03-14 contains information about over 16,000 drugs).

The assignment consists of analyzing the content of the reduced database and creating various tables and charts summarizing the content of the drug database.

1) Create a data frame that, for each drug, contains the following information: a unique identifier for the drug in the DrugBank database, the drug name, its type, description, dosage form, indications, mechanism of action, and information on which foods interact with the drug. (4 pts)

2) Create a data frame that allows searching by DrugBank ID for information on all the synonyms under which a drug appears. Write a function that, for a given DrugBank ID, creates and plots a synonym graph using the NetworkX library. Ensure the readability of the generated plot. (4 pts)

3) Create a data frame for pharmaceutical products that contain a given drug (pharmaceutical substance). The data frame should include information on the drug ID, product name, manufacturer, US National Drug Code (NDC), dosage form, method of administration, dose information, country, and the regulatory agency. (4 pts)

4) Create a data frame containing information on all pathways of all types, e.g., signaling, metabolic, etc., with which any drug interacts. Provide the total number of these pathways. (4 pts)

5) For each signaling/metabolic pathway in the database, list the drugs that interact with it. Present the results in the form of a data frame and also in a self-designed graphical form. An example of such a graphic could be a bipartite graph, where one type of vertex represents signaling pathways and the other drugs, with individual edges representing the interaction between a given drug and a given signaling pathway. Ensure the readability and visual appeal of the graphical presentation. (4 pts)

6) For each drug in the database, provide the number of pathways with which the drug interacts. Present the results in the form of a histogram with appropriately labeled axes. (4 pts)

7) Create a data frame containing information on the proteins with which each drug interacts. These proteins are called targets. The data frame should include at least the target’s DrugBank ID, information about the external database (source, e.g., Swiss-Prot), the identifier in the external database, the polypeptide name, the gene name encoding the polypeptide, the GenAtlas gene ID, the chromosome number, and the subcellular location. (4 pts)

8) Create a pie chart presenting the percentage distribution of targets in different parts of the cell. (4 pts)

9) Create a data frame showing how many drugs have been approved, withdrawn, are in the experimental phase (experimental or investigational), and are approved for veterinary use. Present these data in a pie chart. Provide the number of approved drugs that have not been withdrawn. (4 pts)

10) Create a data frame containing information about potential interactions of a given drug with other drugs. (4 pts)

11) Develop your own graphical presentation containing information about a specific gene or genes, the drugs (pharmaceutical substances) that interact with that gene/gene products, and the pharmaceutical products that contain a given pharmaceutical substance. Whether the presentation is made for a specific gene or for all genes simultaneously is left to your discretion. When choosing, consider the clarity and visual appeal of the presentation. (7 pts)

12) Propose your own analysis and presentation of data concerning drugs. In doing so, you can retrieve additional information from other biomedical and bioinformatics databases available online. However, ensure that the database in question permits automated data retrieval by a program. For example, the GeneCards database explicitly prohibits this, as highlighted in red on its website. Example databases include: UniProt (https://www.uniprot.org/), the Small Molecule Pathway Database (https://smpdb.ca/), and The Human Protein Atlas (https://www.proteinatlas.org/). (7 pts)

13) Create a simulator that generates a test database of 20,000 drugs. The values generated for 19,900 drugs in the “DrugBank Id” column should have consecutive numbers, and in the other columns, values drawn randomly from those existing for the 100 drugs. Save the results in the file drugbank_partial_and_generated.xml. Perform the analysis according to points 1-12 on the test database. (7 pts)

14) Prepare unit tests using the pytest library. (7 pts)

15) Implement point 6 such that it is possible to send a drug ID to your server, which will return the result in the response (using FastAPI and uvicorn; it is sufficient to demonstrate data submission via POST as shown in the Execute section of the documentation). (4 pts)