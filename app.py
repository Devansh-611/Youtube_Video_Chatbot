import os

import streamlit as st
from dotenv import load_dotenv
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import OpenAIEmbeddings
from langchain_openrouter import ChatOpenRouter
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

st.title("Youtube Video Chatbot")


video_id = st.text_input(
    "enter the video id here",
    placeholder="Example: JIWlu7dwDdf",
)


if st.button("save"):
    if not video_id.strip():
        st.warning("enter the valid user id")
    else:
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id)
            transcript = " ".join([chunk.text for chunk in transcript_list.snippets])
        except:
            st.write("unable to load transcript")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.create_documents([transcript])

        embed_model = OpenAIEmbeddings(
            model="nvidia/nemotron-3-embed-1b:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            tiktoken_enabled=False,
            check_embedding_ctx_length=False,
        )

        vector_store = FAISS.from_documents(docs, embed_model )

        st.session_state.vector_store = vector_store
        st.success("Video saved successfully!")


st.write("Ask your question realted to video")
question = st.text_input("Enter text here")

if st.button("search"):
    if "vector_store" not in st.session_state:
        st.warning("Please save a video first")
    elif not question.strip():
        st.warning("please enter a question first")
    else:
        vector_store = st.session_state.vector_store
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )
        prompt = PromptTemplate(
            template="""
you are a helpfule assistant,
Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question :{question}""",
            input_variables=["context", "question"],
        )

        def fun(retrieved_docs):
            context = " ".join([document.page_content for document in retrieved_docs])
            return context

        parser = StrOutputParser()

        chain1 = RunnableParallel(
            {
                "context": retriever | RunnableLambda(fun),
                "question": RunnablePassthrough(),
            }
        )

        chat_llm = ChatOpenRouter(
            model="nvidia/nemotron-3-super-120b-a12b:free",
        )

        final_chain = chain1 | prompt | chat_llm | parser

        if question == "exit":
            st.stop()
        st.write(final_chain.invoke(question))
