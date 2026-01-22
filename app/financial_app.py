import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Financial Doc Chat", page_icon="📈")

st.title("📈 Financial Doc AI Analyst")
st.markdown("""
Upload a Financial Statement (PDF) or a Legal Contract and ask questions.
**Tech Stack:** Streamlit | LangChain | OpenAI | FAISS
""")

# --- SIDEBAR: CONFIG & UPLOAD ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# --- MAIN LOGIC ---

if uploaded_file is not None and api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # 1. Save uploaded file to a temporary file (required for PyPDFLoader)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        with st.spinner("Analyzing document... (Embedding)"):
            # 2. Load PDF
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            # 3. Split Text (Chunking)
            # We split text into smaller chunks to fit into the AI's context window
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)

            # 4. Create Vector Store (The "Brain")
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_documents(chunks, embeddings)

            # 5. Setup the Retrieval Chain
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever()
            )
        
        st.success("Document processed! Ask your questions below.")

        # --- CHAT INTERFACE ---
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Ex: What is the total revenue for 2024?"):
            # Display user message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Run the RAG Chain
                    response = qa_chain.run(prompt)
                    st.markdown(response)
            
            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Cleanup temp file
        os.remove(tmp_file_path)

elif not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
