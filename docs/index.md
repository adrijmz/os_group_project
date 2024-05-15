[![DOI](https://zenodo.org/badge/783363515.svg)](https://zenodo.org/doi/10.5281/zenodo.11200165)


# Repository Overview

The project aims to create a knowledge graph by extracting information from articles. It provides functionalities to extract metadata, process data from Wikidata and OpenAlex, perform topic modeling, and create a knowledge graph. The project can be installed either using Docker or from the source. To extract all information the script use the service GROBID (2008-2022) <https://github.com/kermitt2/grobid>, Wikidata <https://www.wikidata.org/wiki/Wikidata:Main_Page> and OpenAlex <https://openalex.org>.

## Features

- Extraction of metadata from articles using GROBID.
- Processing data from Wikidata and OpenAlex.
- Topic modeling functionality.
- Creation of a knowledge graph.
- API for querying the knowledge graph.

# Install
First of all, clone the repository
```bash
git clone https://github.com/adrijmz/os_group_project.git
```

## Using Docker
To install the GROBID image, execute the following command
```bash
docker pull lfoppiano/grobid:0.7.2
```

To build the extractor image, execute the followint command from the root directory of the repository
```bash
cd /root/directory/of/os_group_project
docker build -t paper_kg .
```

## From Source
To install the GROBID image, execute the following command
```bash
docker pull lfoppiano/grobid:0.7.2
```

### Install Python Environment
This project requires Python 3.8

### Step 1
Create a virtual environment to isolate the project dependencies
```bash
conda create -n myenv python=3.8
```
Init the environment created if it is necessary
```bash
conda init myenv
```
Activate the new environment
```bash
conda activate myenv
```

### Step 2
Install dependencies
```bash
cd /path/to/root/directory/of/os_group_project
pip install -r requirements.txt
```

# Usage
## Using Docker
Create a Docker network to communicate both containers
```bash
docker network create kg_red
```

To run the GROBID container, execute the following command
```bash
docker run --name server --network kg_red -p 8070:8070 lfoppiano/grobid:0.7.2
```
**<span style="text-decoration: underline;">Before running the app, check in src/functionalities/grobid.py that url has this value</span>**

```bash
url = "http://server:8070/api/processFulltextDocument
```

To run the app container, open a new terminal window and execute the following command
```bash
docker run --name paper_kg --network kg_red paper_kg
```

When all scripts have finished executing, access this URL to make queries to the knowledge graph:
```bash
http://127.0.0.1:8050/
```

#### If you want to see the files generated and you have used Docker to run extractor, execute the following command

To check container ID
```bash
docker ps -a
```

To copy all files to a desire directory
```bash
docker cp container_id:/app /path/to/your/directory
```

## From Source

To run the GROBID container, execute the following command
```bash
docker run --name server -p 8070:8070 lfoppiano/grobid:0.7.2
```
**<span style="text-decoration: underline;">Before running the app, check in src/functionalities/grobid.py that url has this value</span>**
```bash
url = "http://localhost:8070/api/processFulltextDocument"
```

To run all scripts (from the root directory) follow this order. You need to have activated the previous conda env.
```bash
python src/functionalities/grobid.py
python src/functionalities/wikidataProcess.py
python src/functionalities/openalex.py
python src/functionalities/abstract_lda.py
python src/functionalities/knowledge_graph.py
python src/api/app.py
```

When app.py script have finished executing, access this URL to make queries to the knowledge graph:
```bash
http://127.0.0.1:8050/
```

To access the GROBID service, go to the following URL
- http://localhost:8070/

# Examples to query

To obtain all titles:
```bash
PREFIX schema: <http://schema.org/>
    SELECT ?title
    WHERE {
        ?paper a schema:paper ;
               schema:title ?title .
    }
```

To obtain all possible topics:
```bash
PREFIX schema: <http://schema.org/>
    SELECT ?topic
    WHERE {
        ?paper a schema:topic ;
               schema:name ?topic .
    }
```

To obtain a specific paper:
```bash
PREFIX schema: <http://schema.org/>

    SELECT ?title ?topic ?author
    WHERE {
    ?paper a schema:paper ;
        schema:doi "10.26735/TLYG7256" ;
        schema:title ?title ;
        schema:topic ?topic ;
        schema:author ?author .
    }
```