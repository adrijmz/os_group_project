import csv
import os
from qwikidata.sparql  import return_sparql_query_results
from time import sleep

def query_wikidata(doi):

    # Realizar la consulta SPARQL
    query = f"""
    SELECT DISTINCT ?title ?doi ?published_in ?cites ?num_pag ?pages ?publication_date ?language ?instance_of ?main_subject
WHERE {{
    ?paper wdt:P356 "{doi}".
    ?paper rdfs:label ?title.
    FILTER (LANG(?title) = "en").
    OPTIONAL {{ ?paper wdt:P356 ?doi. }}
    OPTIONAL {{ ?paper wdt:P1433 ?published_in. }}
    OPTIONAL {{ ?paper wdt:P2860 ?cites. }}
    OPTIONAL {{ ?paper wdt:P1104 ?num_pag. }}
    OPTIONAL {{ ?paper wdt:P304 ?pages. }}
    OPTIONAL {{ ?paper wdt:P577 ?publication_date. }}
    OPTIONAL {{ ?paper wdt:P407 ?language. }}
    OPTIONAL {{ ?paper wdt:P31 ?instance_of. }}
    OPTIONAL {{ ?paper wdt:P921 ?main_subject. }}
}}
LIMIT 1
    """
    result = return_sparql_query_results(query)
    print(result)

    # Devolver resultados
    return result['results']['bindings']

def main():
    # Ruta para guardar el archivo CSV
    output_path = '../../papers/wikidata/results.csv'

    # Crear la carpeta para guardar los resultados si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Abrir el archivo CSV en modo escritura
    with open(output_path, 'w', newline='') as csv_file:
        # Definir los encabezados del archivo CSV
        fieldnames = ['Title', 'DOI', 'Cites', 'Number of Pages', 'Publication Date', 'Language', 'Pages', 'Published In', 'Main Subject', 'Instance Of']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterar sobre los archivos en la carpeta de títulos
        titles_folder = '../../papers/doi/'
        for filename in os.listdir(titles_folder):
            if filename.endswith('.txt'):
                # Leer los títulos del archivo
                with open(os.path.join(titles_folder, filename), 'r') as file:
                    dois = [line.strip() for line in file.readlines()]

                # Iterar sobre los títulos y realizar la consulta para cada uno
                for doi in dois:
                    results = query_wikidata(doi)
                    if results:
                        # Escribir los resultados en el archivo CSV
                        for result in results:
                            writer.writerow({
                                'Title': result.get('title', {}).get('value', 'N/A'),
                                'DOI': result.get('doi', {}).get('value', 'N/A'),
                                'Cites': result.get('cites', {}).get('value', 'N/A'),
                                'Number of Pages': result.get('num_pag', {}).get('value', 'N/A'),
                                'Publication Date': result.get('publication_date', {}).get('value', 'N/A'),
                                'Language': result.get('language', {}).get('value', 'N/A'),
                                'Pages': result.get('pages', {}).get('value', 'N/A'),
                                'Published In': result.get('published_in', {}).get('value', 'N/A'),
                                'Main Subject': result.get('main_subject', {}).get('value', 'N/A'),
                                'Instance Of': result.get('instace_of', {}).get('value', 'N/A')
                            })
                    sleep(1)

    print("Results have been saved to", output_path)

if __name__ == "__main__":
    main()
