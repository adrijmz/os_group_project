[![DOI](https://zenodo.org/badge/783363515.svg)](https://zenodo.org/doi/10.5281/zenodo.11200165)

Our application endeavors to revolutionize  research by constructing a comprehensive knowledge graph sourced from articles. Featuring robust functionalities, including metadata extraction, data processing from Wikidata and OpenAlex, topic modeling, and knowledge graph creation, users can seamlessly navigate and explore intricate connections within scholarly literature. Installation options via Docker or from the source ensure accessibility and flexibility for all users.

## Goals

- Create a knowledge graph from articles to facilitate access and understanding of the information contained within them.
- Automate the extraction of metadata and creation of relationships between articles to generate an information-rich graph.

## Features Overview

- Extraction of metadata from academic articles using GROBID.
- Processing data from Wikidata and OpenAlex to enrich the knowledge graph.
- Topic modeling functionality to identify the main themes of articles.
- Creation of a knowledge graph representing relationships between articles and topics.
- API for querying and accessing information from the knowledge graph.

## Technical Approach

- Utilize GROBID to extract metadata from academic articles such as title, author, publication date, etc.
- Process data from Wikidata and OpenAlex to obtain additional information about authors and article topics.
- Implement topic modeling techniques such as LDA to identify the main themes of articles.
- Utilize RDF and SPARQL to represent and query the generated knowledge graph.

## Potential Impact

- Facilitate access and comprehension of the vast amount of information contained in academic articles.
- Enable researchers and students to perform complex queries on specific topics within the study domain.
- Facilitate the identification of connections and relationships between different articles and topics, leading to new discoveries and research avenues.