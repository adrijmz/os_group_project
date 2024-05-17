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
- http://127.0.0.1:8050/


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
- http://127.0.0.1:8050/


To access the GROBID service, go to the following URL
- http://localhost:8070/