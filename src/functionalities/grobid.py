import os
import requests
import argparse


def extract_metadata_pdf(pdf_path):

    # uncomment the following line to use the server instead of the local grobid (docker bridge network must be created)
    # url = "http://server:8070/api/processFulltextDocument"
    url = "http://localhost:8070/api/processFulltextDocument"
    files = {'input': open(pdf_path, 'rb')}
    headers = {}

    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Error al procesar el archivo:", pdf_path)
        return None
    
def delete_labels_from_abstract(text):
    # Eliminar las etiquetas HTML del text
    while True:
        start = text.find("<")
        if start == -1:
            break
        end = text.find(">", start)
        if end == -1:
            break
        text = text[:start] + text[end + 1:]
    return text

def main(folder_path, output_directory):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            metadata_xml = extract_metadata_pdf(pdf_path)
            if metadata_xml:
                # Guardar los metadatos en un archivo XML en la carpeta xml
                xml_filename = os.path.splitext(filename)[0] + ".xml"
                xml_path = os.path.join(output_directory, xml_filename)
                with open(xml_path, "w") as xml_file:
                    xml_file.write(metadata_xml)

# read every xml file to get the title and save it in a .txt file
def get_metadata_fron_xml(xml_directory, title_directory, abstract_directory, acknowledgements_directory):
    for filename in os.listdir(xml_directory):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_directory, filename)
            with open(xml_path, "r") as xml_file:
                xml_content = xml_file.read()
                doi_start = xml_content.find('<idno type="DOI">') + len('<idno type="DOI">')
                doi_end = xml_content.find('</idno>', doi_start)
                doi = xml_content[doi_start:doi_end]
                doi = doi.upper()


                # Guardar el título en un archivo .txt en la carpeta titles
                title_filename = os.path.splitext(filename)[0] + ".txt"
                title_path = os.path.join(title_directory, title_filename)
                with open(title_path, "w") as title_file:
                    title_file.write(doi)

                abstract_start = xml_content.find('<abstract>')
                if(abstract_start != -1):
                    abstract_start += len('<abstract>')
                    abstract_end = xml_content.find('</abstract>')
                    abstract = xml_content[abstract_start:abstract_end]
                    abstract = delete_labels_from_abstract(abstract)
                    # Guardar el abstract en un archivo .txt en la carpeta abstract
                    abstract_filename = os.path.splitext(filename)[0] + ".txt"
                    abstract_path = os.path.join(abstract_directory, abstract_filename)
                    with open(abstract_path, "w") as abstract_file:
                        abstract_file.write(abstract)
                
                acknowledgements_start = xml_content.find('<div type="acknowledgement">')
                if acknowledgements_start != -1:
                    acknowledgements_start += len('<div type="acknowledgement">')
                    acknowledgements_end = xml_content.find('</div>', acknowledgements_start)
                    acknowledgements = xml_content[acknowledgements_start:acknowledgements_end]
                    acknowledgements = delete_labels_from_abstract(acknowledgements)
                    # Guardar el acknowledgement en un archivo .txt en la carpeta acknowledgements
                    acknowledgements_filename = os.path.splitext(filename)[0] + ".txt"
                    acknowledgements_path = os.path.join(acknowledgements_directory, acknowledgements_filename)
                    with open(acknowledgements_path, "w") as acknowledgements_file:
                        acknowledgements_file.write(acknowledgements)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='grobid.py',
        description='Process some PDFs.')
    
    parser.add_argument(
        '--INPUT',
        default='papers/pdf/',
        type=str,
        help='Directory containing PDFs')

    parser.add_argument(
        '--OUTPUT',
        default='papers/xml/',
        type=str,
        help='Directory to save the output files')

    args = parser.parse_args()
    pdf_directory = args.INPUT
    xml_directory = args.OUTPUT
    title_directory = 'papers/doi/'
    abstract_directory = 'papers/abstract/'
    acknowledgements_directory = 'papers/acknowledgements/'

    # Crear la carpeta de salida si no existe
    os.makedirs(xml_directory, exist_ok=True)
    os.makedirs(title_directory, exist_ok=True)
    os.makedirs(abstract_directory, exist_ok=True)
    os.makedirs(acknowledgements_directory, exist_ok=True)
    main(pdf_directory, xml_directory)
    get_metadata_fron_xml(xml_directory, title_directory, abstract_directory, acknowledgements_directory)
