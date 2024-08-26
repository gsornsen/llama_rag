from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.program.openai import OpenAIPydanticProgram
import openai
from pydantic import BaseModel
from utils import get_openai_api_key


class WikiPageList(BaseModel):
    "Data model for WikiPageList"
    pages: list[str]


def wikipage_list(query: str) -> WikiPageList:
    openai.api_key = get_openai_api_key()

    prompt_template_str = """
    Given the input {query},
    extract the Wikipedia pages mentioned after
    "please index:" and return them as a list.
    If only one page is mentioned, return a single
    element list.
    """
    program = OpenAIPydanticProgram.from_defaults(
        output_cls=WikiPageList,
        prompt_template_str=prompt_template_str,
        verbose=True,
    )
    wikipage_requests = program(query=query)
    return wikipage_requests


def create_wikidocs(wikipage_requests: WikiPageList) -> list:
    reader = WikipediaReader()
    documents = reader.load_data(pages=wikipage_requests)
    return documents


def create_index(query: str) -> VectorStoreIndex:
    wikipage_requests = wikipage_list(query)
    wikidocs = create_wikidocs(wikipage_requests)
    text_splitter = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=45,
    )
    nodes = text_splitter.get_nodes_from_documents(wikidocs)
    index = VectorStoreIndex(nodes)
    return index
