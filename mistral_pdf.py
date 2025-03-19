#!/usr/bin/env python3

import os
import sys
import json
from time import sleep
from dotenv import load_dotenv
from mistralai import Mistral

def upload_document(client, file_path):
    """
    Uploads the PDF document to be processed by the OCR service.

    Args:
        client (Mistral): The instantiated Mistral client.
        file_path (str): The path to the PDF file.

    Returns:
        str: A signed URL for accessing the uploaded document.
    """
    uploaded_pdf = client.files.upload(
        file={
            "file_name": file_path,
            "content": open(file_path, 'rb'),
        },
        purpose='ocr'
    )
    sleep(3)  # Allow the file to be processed and lower our request rate.
    # Get a signed URL that allows us to access the uploaded file with a 1 hour expiration.
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id, expiry=1)
    return signed_url.url

def read_document(client, signed_url):
    """
    Reads and processes the document via OCR using the provided signed URL.

    Args:
        client (Mistral): The instantiated Mistral client.
        signed_url (str): The signed URL of the uploaded document.

    Returns:
        dict: The OCR response converted from JSON to a dictionary.
    """
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url
        }
    )
    return json.loads(ocr_response.model_dump_json())

def merge_markdown(ocr_response, output_file):
    """
    Extracts the Markdown from each page in the OCR response,
    prefixes each section with a page marker, and writes the combined
    content to the specified output file.

    Args:
        ocr_response (dict): The OCR response containing page data.
        output_file (str): The file path where the merged markdown will be saved.
    """
    merged_lines = []
    for page in ocr_response.get("pages", []):
        merged_lines.append(f"## Page {page.get('index', '?')}\n")
        merged_lines.append(page.get("markdown", ""))
        merged_lines.append("\n---\n")
    
    with open(output_file, "w") as f:
        f.write("\n".join(merged_lines))
    print(f"Merged markdown saved to {output_file}")

def main():
    """
    Main execution function.
    
    Loads environment variables and the Mistral API key, initializes the Mistral client,
    uploads the document, processes it using OCR, and saves the resulting Markdown in a file
    derived from the input document's filename.
    """
    load_dotenv()
    api_key = os.getenv('MISTRAL_API_KEY')
    client = Mistral(api_key=api_key)
    file_path = sys.argv[1]
    
    signed_url = upload_document(client, file_path)
    response_dict = read_document(client, signed_url)
    data = json.dumps(response_dict, indent=4)
    
    # Create the output Markdown file name based on the input file's basename.
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    # Output file will be saved in the same directory as the input file.
    output_file = f"{base_filename}.md"
    # Merge the extracted Markdown content and save it to the output file.
    merge_markdown(response_dict, output_file)

if __name__ == '__main__':
    main()