# MistralPDF

MistralPDF is a Python script for interacting with the [Mistral OCR API](https://docs.mistral.ai/capabilities/document/) to process your PDF files and generate Markdown output.

## Features

- Extract text from PDF files using the Mistral OCR API.
- Generate output in Markdown format.

## Setup

### 1. Obtain API Key

- Get a valid API key from [Mistral](https://mistral.ai/).
- Create a `.env` file and add your API key:
  ```env
  MISTRAL_API_KEY=your_api_key_here
  ```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment:
```sh
python3 -m venv env
source ./env/bin/activate
```

### 3. Install Dependencies

Install the required packages:
```sh
pip install -r requirements.txt
```

## Usage

Run the script with a PDF file as the argument:
```sh
python3 mistralpdf.py <filename>
```

## Contributing

Contributions are welcome! Open issues or submit pull requests for suggestions and improvements.