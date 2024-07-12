from indexify import ExtractionGraph, IndexifyClient
import requests
from indexify import IndexifyClient
from indexify import IndexifyClient

client = IndexifyClient()

extraction_graph_spec = """
name: 'pdfqa'
extraction_policies:
  - extractor: 'tensorlake/marker'  (2)!
    name: 'mdextract'
  - extractor: 'tensorlake/chunk-extractor' (3)!
    name: 'chunker'
    input_params:
        chunk_size: 1000
        overlap: 100
    content_source: 'mdextract'
  - extractor: 'tensorlake/minilm-l6' (4)!
    name: 'pdfembedding'
    content_source: 'chunker'
"""
extraction_graph = ExtractionGraph.from_yaml(extraction_graph_spec)
client.create_extraction_graph(extraction_graph)

client = IndexifyClient()

response = requests.get("https://www.loc.gov/item/2020445568/")
with open("taxes.pdf", 'wb') as file:
    file.write(response.content)

client.upload_file("pdfqa", "taxes.pdf")from openai import OpenAI

client = IndexifyClient()
client_openai = OpenAI()

def get_context(question: str, index: str, top_k=3):
    results = client.search_index(name=index, query=question, top_k=3)
    context = ""
    for result in results:
        context = context + f"content id: {result['content_id']} \n\n passage: {result['text']}\n"
    return context
def create_prompt(question, context):
    return f"Answer the question, based on the context.\n question: {question} \n context: {context}"

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
