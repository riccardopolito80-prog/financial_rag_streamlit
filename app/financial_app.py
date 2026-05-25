import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

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

# Inizializza lo stato della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN LOGIC ---
if uploaded_file is not None and api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Processa il documento SOLO SE non è già stato salvato in session_state
    if "qa_chain" not in st.session_state:
        try:
            with st.spinner("Analyzing document... (Embedding)"):
                # 1. Salva in un file temporaneo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                try:
                    # 2. Carica ed elabora il PDF
                    loader = PyPDFLoader(tmp_file_path)
                    documents = loader.load()

                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    chunks = text_splitter.split_documents(documents)

                    # 3. Crea il Vector Store
                    embeddings = OpenAIEmbeddings()
                    vector_store = FAISS.from_documents(chunks, embeddings)
                    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

                    # 4. Configura la nuova catena (Modern LangChain)
                    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
                    
                    system_prompt = (
                        "You are an expert financial analyst. Use the following pieces of retrieved context "
                        "to answer the question. If you don't know the answer, say that you don't know.\n\n"
                        "{context}"
                    )
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ])
                    
                    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
                    # Salviamo la catena finale nello stato di Streamlit
                    st.session_state.qa_chain = create_retrieval_chain(retriever, question_answer_chain)
                    st.success("Document processed successfully!")
                    
                finally:
                    # Pulizia del file temporaneo sicura dopo la lettura
                    if os.path.exists(tmp_file_path):
                        os.remove(tmp_file_path)
                        
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")

    # --- CHAT INTERFACE ---
    # Mostra la cronologia se la catena è pronta
    if "qa_chain" in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Gestione dell'input utente
        if prompt := st.chat_input("Ex: What is the total revenue for 2024?"):
            # Mostra e salva il messaggio dell'utente
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Genera la risposta
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Utilizzo del nuovo metodo .invoke()
                        response = st.session_state.qa_chain.invoke({"input": prompt})
                        answer = response["answer"]
                        st.markdown(answer)
                        # Salva la risposta dell'assistente
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Error generating response: {e}")

elif not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")

      
