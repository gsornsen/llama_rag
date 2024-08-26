from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import chainlit as cl
from chainlit.input_widget import Select, TextInput
import openai
from index_wikipages import create_index
from utils import get_openai_api_key


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("index", None)
    cl.user_session.set("agent", None)
    await cl.ChatSettings(
        [
            Select(
                id="MODEL",
                label="OpenAI Model",
                values=["gpt-4o", "gpt-3.5-turbo"],
                initial_index=0,
            ),
            TextInput(
                id="WikiPageRequest",
                label="Request Wikipage",
            ),
        ]
    ).send()


def wikisearch_engine(index):
    Settings.context_window = 3900
    query_engine = index.as_query_engine(
        streaming=True,
        response_mode="compact",
        verbose=True,
        similarity_top_k=10,
    )
    cl.user_session.set("query_engine", query_engine)
    return query_engine


def create_react_agent(MODEL, index):
    query_engine_tools = [
        QueryEngineTool(
            query_engine=wikisearch_engine(index),
            metadata=ToolMetadata(
                name="Wikipedia",
                description="Useful for performing searches on Wikipedia",
            ),
        )
    ]

    openai.api_key = get_openai_api_key()
    llm = OpenAI(model=MODEL)
    agent = ReActAgent.from_tools(
        tools=query_engine_tools,
        llm=llm,
        verbose=True,
    )
    return agent


@cl.on_settings_update
async def setup_agent(settings):
    query = settings["WikiPageRequest"]
    if not isinstance(query, str):
        query = str(query)
    index = create_index(query)
    cl.user_session.set("index", index)
    print(f"Index created for query: {query}")
    print(f"on_settings_update: {settings}")
    MODEL = settings["MODEL"]
    if not isinstance(MODEL, str):
        MODEL = str(MODEL)
    agent = create_react_agent(MODEL, index)
    cl.user_session.set("agent", agent)
    await cl.Message(
        author="Agent",
        content=f"""Wikipage(s) "{query} successfully indexed""",
    ).send()


@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")
    msg = cl.Message(content="", author="Assistant")
    response = await cl.make_async(query_engine.query)(message.content)
    for token in response.response_gen:
        await msg.stream_token(token)
    await msg.send()
