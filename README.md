# Wikipedia Chat Agent

This project implements a conversational agent that can automatically index Wikipedia pages on demand and use RAG (Retrieval-Augmented Generation) methodology with OpenAI to chat about the indexed articles.

## Demo
![](https://github.com/gsornsen/llama_rag/blob/main/media/llama_rag.gif)

## Features

- On-demand indexing of Wikipedia pages
- RAG-based chatbot using OpenAI and LlamaIndex
- Interactive UI powered by Chainlit

## Setup

1. Clone the repository
2. Create a virtual environment:

```bash
make env
```

3. Run the application:

```
make run
```

## Usage

1. Open a web browser and navigate to `http://localhost:8000`
2. Enter "please index: Wikipedia Page Title or Titles" in the settings Modal
3. The agent will automatically index the relevant Wikipedia page(s) and be ready for you to ask questions about the content in the article(s)

## Technical Details

The application uses the following components:

- LlamaIndex: A Python library for building and querying large language models
- OpenAI: A cloud-based AI platform for generating human-like text
- Chainlit: A Python library for building interactive web applications

The RAG methodology is used to generate responses to user queries by retrieving relevant information from the indexed Wikipedia pages and generating text based on that information.
