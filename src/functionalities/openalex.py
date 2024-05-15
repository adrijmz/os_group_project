import csv
import os
import requests
from time import sleep

def query_openalex(doi):
    url = "https://api.openalex.org/works?search="+doi

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def main():
    # Ruta para guardar el archivo CSV
    output_path = 'papers/openalex/results.csv'

    # Crear la carpeta para guardar los resultados si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Abrir el archivo CSV en modo escritura
    with open(output_path, 'w', newline='') as csv_file:
        # Definir los encabezados del archivo CSV
        fieldnames = ['DOI', 'Name', 'Institution']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterar sobre los archivos en la carpeta de títulos
        dois_files = 'papers/doi/'
        for filename in os.listdir(dois_files):
            if filename.endswith('.txt'):
                # Leer los títulos del archivo
                with open(os.path.join(dois_files, filename), 'r') as file:
                    doi = file.read()
                
                results = query_openalex(doi)

                if results:
                    # Escribir los resultados en el archivo CSV solo del primer resultado
                    for result in results['results']:
                        authorships = result.get('authorships', [])
                        for author in authorships:
                            name = author.get('author').get('display_name')
                            
                            intitutions = author.get('institutions', [])

                            if intitutions:
                                for institution in intitutions:
                                    writer.writerow({
                                        'DOI': doi,
                                        'Name': name,
                                        'Institution': institution.get('display_name')
                                    })
                            else:
                                writer.writerow({
                                    'DOI': doi,
                                    'Name': name,
                                    'Institution': 'N/A'
                                })
                        break
                sleep(1)

    print("Results have been saved to", output_path)     

if __name__ == "__main__":
    main()
    