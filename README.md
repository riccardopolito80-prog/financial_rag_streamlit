# financial_rag_streamlit
# 📈 Financial Document Chat (RAG)

A clean, Python-based RAG (Retrieval-Augmented Generation) application designed to analyze financial statements, contracts, and legal documents.

Built with **Streamlit** for the frontend and **LangChain** for the orchestration logic.

## 🚀 Features
* **Instant Analysis:** Upload any PDF (Balance Sheets, Invoices, Contracts).
* **Vector Search:** Uses FAISS to index document chunks for semantic retrieval.
* **Q&A Interface:** Chat with your document using OpenAI GPT-4o models.
* **Privacy:** Documents are processed in memory/temp storage and not permanently saved.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** Streamlit
* **AI Orchestration:** LangChain
* **Embeddings:** OpenAI text-embedding-3-small
* **Vector DB:** FAISS (Local CPU version)

## 📦 How to Run

1. **Clone the repo**
   ```bash
   git clone [https://github.com/yourusername/financial-rag-streamlit.git](https://github.com/yourusername/financial-rag-streamlit.git) or install all the files,install the requirements and create a venv.
   cd financial-rag-streamlit
