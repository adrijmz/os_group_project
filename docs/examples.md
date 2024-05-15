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