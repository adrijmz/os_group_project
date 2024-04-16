import os
import requests
import argparse


def extract_metadata_pdf(pdf_path):
    url = "http://localhost:8070/api/processHeaderDocument"
    files = {'input': open(pdf_path, 'rb')}
    headers = {}

    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Error al procesar el archivo:", pdf_path)
        return None

def main(folder_path, output_directory):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            metadata_xml = extract_metadata_pdf(pdf_path)
            if metadata_xml:
                # Aquí puedes procesar el XML de metadatos según tus necesidades
                print("Metadatos extraídos de:", pdf_path)
                print(metadata_xml)
                print("="*50)
                # Guardar los metadatos en un archivo XML en la carpeta xml
                xml_filename = os.path.splitext(filename)[0] + ".xml"
                xml_path = os.path.join(output_directory, xml_filename)
                with open(xml_path, "w") as xml_file:
                    xml_file.write(metadata_xml)

# read every xml file to get the title and save it in a .txt file
def get_title_from_xml(xml_directory, title_directory):
    for filename in os.listdir(xml_directory):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_directory, filename)
            with open(xml_path, "r") as xml_file:
                xml_content = xml_file.read()
                title_start = xml_content.find('<title level="a" type="main">') + len('<title level="a" type="main">')
                title_end = xml_content.find("</title>")
                title = xml_content[title_start:title_end]
                
                # Guardar el título en un archivo .txt en la carpeta titles
                title_filename = os.path.splitext(filename)[0] + ".txt"
                title_path = os.path.join(title_directory, title_filename)
                with open(title_path, "w") as title_file:
                    title_file.write(title)

    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='grobid.py',
        description='Process some PDFs.')
    
    parser.add_argument(
        '--INPUT',
        default='./papers/pdf/',
        type=str,
        help='Directory containing PDFs')

    parser.add_argument(
        '--OUTPUT',
        default='./papers/xml/',
        type=str,
        help='Directory to save the output files')

    args = parser.parse_args()
    pdf_directory = args.INPUT
    xml_directory = args.OUTPUT
    title_directory = './papers/titles/'

    # Crear la carpeta de salida si no existe
    os.makedirs(xml_directory, exist_ok=True)
    os.makedirs(title_directory, exist_ok=True)
    main(pdf_directory, xml_directory)
    get_title_from_xml(xml_directory, title_directory)
