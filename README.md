
# PDF Tax Information Extraction and Question Answering

This project demonstrates how to use the `indexify` library to extract and query information from a PDF document using various extractors and models. The workflow includes setting up an extraction graph, uploading a PDF file, and querying the extracted content for specific information.

## Prerequisites
```
- Python 3.6 or later
- `indexify` library
- `requests` library
- `openai` library

## Setup

1. **Install the required libraries:**

```bash
pip install indexify requests openai
```

2. **Download the PDF file:**

The PDF file will be downloaded from a specified URL and saved locally.

## Usage

1. **Import necessary libraries:**

```python
from indexify import ExtractionGraph, IndexifyClient
import requests
from openai import OpenAI
```

2. **Create an Indexify client:**

```python
client = IndexifyClient()
client_openai = OpenAI()
```

3. **Define the extraction graph:**

This extraction graph uses three extractors: `tensorlake/marker`, `tensorlake/chunk-extractor`, and `tensorlake/minilm-l6`.

```python
extraction_graph_spec = """
name: 'pdfqa'
extraction_policies:
  - extractor: 'tensorlake/marker'
    name: 'mdextract'
  - extractor: 'tensorlake/chunk-extractor'
    name: 'chunker'
    input_params:
        chunk_size: 1000
        overlap: 100
    content_source: 'mdextract'
  - extractor: 'tensorlake/minilm-l6'
    name: 'pdfembedding'
    content_source: 'chunker'
"""
extraction_graph = ExtractionGraph.from_yaml(extraction_graph_spec)
client.create_extraction_graph(extraction_graph)
```

4. **Download and upload the PDF file:**

```python
response = requests.get("https://www.loc.gov/item/2020445568/")
with open("taxes.pdf", 'wb') as file:
    file.write(response.content)

client.upload_file("pdfqa", "taxes.pdf")
```

5. **Define a function to get context from the index:**

```python
def get_context(question: str, index: str, top_k=3):
    results = client.search_index(name=index, query=question, top_k=top_k)
    context = ""
    for result in results:
        context = context + f"content id: {result['content_id']} \n\n passage: {result['text']}\n"
    return context
```

6. **Define a function to create the prompt for the model:**

```python
def create_prompt(question, context):
    return f"Answer the question, based on the context.\n question: {question} \n context: {context}"
```

7. **Ask a question and get the answer:**

```python
question = "What are the tax brackets in California and how much would I owe on an income of $24,000?"
context = get_context(question, "pdfqa.pdfembedding.embedding")

prompt = create_prompt(question, context)

chat_completion = client_openai.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)
```

## Conclusion

This project demonstrates how to extract, query, and use information from a PDF document using the `indexify` library and OpenAI's GPT model. The code provides a framework for similar tasks involving document analysis and question answering.

## License

This project is licensed under the MIT License.
```
```
