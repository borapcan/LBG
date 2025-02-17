# The Library of Brain Glycans (LBG) User Guide

The [Library of Brain Glycans (LBG)](https://lbg.human-glycome.org/) is a freely accessible database designed to assist researchers in exploring the composition, structure, and biological context of brain glycans. It integrates mass spectrometry and liquid chromatography data, allowing searches by species, brain region, and developmental stage. The LBG is an initiative of the [Human Glycome Project](https://human-glycome.org/) whose mission is to catalogue and define the structures and functions of all human glycoconjugates. 

## Accessing the Database

To begin, navigate to the LBG database:

- **URL**: [https://lbg.human-glycome.org/](https://lbg.human-glycome.org/)

---

## Library Design and Structure

![Structure of the database. The diagram illustrates the datatypes, relationships between them, as well as current and future implementations of tables in the database](http://drive.google.com/uc?export=view&id=1nGnsBbzcvA1JiVtCBqiI3rZS4FlndBDa)

The **Library of Brain Glycans (LBG)** is a curated and continuously updated repository designed to facilitate the exploration of glycan structures, compositions, and their biological contexts in the brain. The database is structured to integrate multiple layers of information, including species, developmental stages, brain regions, and analytical data thus allowing researchers to navigate complex glycobiological relationships efficiently.

### Classification and Organization

The LBG is classified based on **data objects, data types, and biological contexts**, ensuring a structured approach to glycan research.

- **Data Object**: The LBG focuses on glycans derived from animal models, particularly rodent brains, with future expansions planned for additional species and cell types.  
- **Data Type**: The database contains data on molecular mass, chromatographic retention values, and glycan composition data, supporting both mass spectrometry-based identification and experimental validation.  
- **Biological Context**: Entries are tagged based on the brain region, species, and life stage to provide a detailed view of glycan distribution and function.  

### Database Structure and Components

The LBG follows a **relational database model**, interconnecting chemical glycan data (such as molecular mass, monosaccharide composition, chromatographic retention time) with biological data on the in situ expression patterns of individual glycans (such as species, brain regions, and life stages). The core elements include:

- **Glycan Entries**: Each glycan is cataloged with its unique ID, monosaccharide composition, mass, and chromatographic properties.  
- **Species and Brain Regions**: Glycans are linked to specific species and brain regions, providing insights into their spatial distribution in situ.  
- **Life Stages**: Data are categorized by age and/or developmental phases, allowing users to explore ontological variation in glycan expression.  
- **References**: Each glycan entry added from a published study is referenced with supporting literature, enabling users to trace its discovery and context.  
- **Diagnostic Fragments**: Where tandem mass spectrometry data are available, the structural motifs associated with particular glycans based on fragmentation analysis are catalogued with the molecular mass, motif identification, and structural representations to support the structural assignment.
- **Pathology (Planned)**: Future updates will integrate pathology-related data, classifying glycans by disease relevance and providing comparative data between healthy and pathological states. This implementation aligns with the growing interest in glycobiology's role in disease mechanisms and will enhance LBG’s utility in translational research.

### Curation and Versioning

To ensure data accuracy and usability, the LBG follows a structured **curation model**:

- **Regular Updates**: The database is actively maintained, with periodic updates incorporating new research findings and refined analytical data.  
- **Versioning Policy**: When major updates occur, past versions remain accessible, allowing researchers to reference the dataset as it was at the time of citation. This ensures reproducibility and consistency in scientific communication.  
- **Curation Standards**: Entries undergo manual verification by expert curators to maintain data integrity, with contributions from researchers encouraged to expand the knowledge base.  

The LBG is committed to maintaining a dynamic yet stable resource for the glycobiology community, balancing **innovation** with **continuity** to support high-quality research.

---

## Searching the Library

### How to search?

1. **Homepage**: Upon accessing the site, you will see the homepage with a search interface.
2. **Search Input**: Enter your query into the search bar. You can search by any of the following parameters:
    - **Glycan ID**: Search by a unique identifier assigned to a glycan.
    - **Species**: Specify the organism of interest.
    - **Brain Region**: Indicate the specific brain region of interest.
    - **Study**: Search for glycans based on associated studies.
    - **All Entries**: To view all entries, leave the search bar **empty** or type a **star (*)**.
3. **Executing the Search**: Press the "Enter" key or click the search icon to execute the search.

### Filtering Options

The LBG database provides extensive filtering capabilities to refine searches based on specific research needs. Users can filter glycans based on:

- **Species**: Select specific organisms such as rats or mice.
- **Brain regions**: Filter by different regions of the brain where the glycan was identified.
- **Stages of Life**: Narrow results to glycans found at specific developmental stages (e.g., neonate, adult).
- **Mass**: Define a range of molecular weights to find glycans with similar masses.
- **GU (Glucose Unit)**: Search based on glucose unit values, which relate to chromatographic retention.

### Results Table

The search results are displayed in a structured tabular format, providing detailed glycan-related data. Each row corresponds to a glycan entry, and the table includes the following columns:

- **Glycan ID**: A unique and randomly assigned identifier for each glycan entry which takes the form LBG-***** (where * can be any number from 0-9 or any standard letter of the English alphabet).
- **Mass**: The molecular weight of the glycan, measured in Daltons.
- **Sialic Acid Derivatization**: Indicates whether the glycan was derivatised during analysis.
- **GU Values**: Displays the minimum, mean, and maximum glucose unit (GU) values reported for each glycan.
- **Monosaccharide Composition**: Lists the molecular composition of each glycan, specifying the number of sugar residues present.
- **Species**: Identifies the species in which the glycan was found (e.g., rat, mouse).
- **References**: Displays published studies in which the glycans were detected.
- **Stages of Life**: Indicates the developmental stage (e.g., neonate, adult) at which the glycan was detected.
- **Sublocation**: Specifies the brain region or cell type in which the glycan was identified.

Users can click on a glycan entry to access additional details, including study references and experimental methods used to identify the glycan.

---

## Additional Resources

- **[About](https://lbg.human-glycome.org/about)**: Learn more about the LBG project and its objectives by visiting the "About" section.
- **[Terms and conditions](https://lbg.human-glycome.org/privacy-policy)**: Familiarize yourself with the terms governing the use of the database.
- **[Privacy policy](https://lbg.human-glycome.org/terms-and-conditions)**: Understand how your data is handled by reviewing the privacy policy.

For further assistance or inquiries, please refer to the contact information provided on the LBG website.

---

## How to Cite, Submit and Contact?

### How to Cite LBG Database?

To cite the Library of Brain Glycans, please refer to the related publication.

Related Publication:

### How to submit your data?

We are in the process of developing a dedicated submission form to streamline the process of contributing research data. In the meantime, researchers interested in submitting their studies or datasets can do so by reaching out to the curators using the contact information provided below.


### Contact Information

**Genos Glycoscience**  
Biocentar,    
Zagreb 10000, Croatia  
**Email**: lbg@genos.hr  
**Tel**: 



*Note: This guide is based on the information available as of February 11, 2025.*