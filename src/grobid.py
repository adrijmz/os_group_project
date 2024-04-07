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
    output_directory = args.OUTPUT

    # Crear la carpeta de salida si no existe
    os.makedirs(output_directory, exist_ok=True)
    main(pdf_directory, output_directory)
