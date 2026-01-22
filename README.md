📊 FinAnalyzer AI (RAG Pipeline)

FinAnalyzer AI è un'applicazione Enterprise-grade di tipo RAG (Retrieval-Augmented Generation) progettata per analizzare documenti finanziari complessi (Bilanci, Contratti, Report) attraverso un'interfaccia di chat conversazionale.

A differenza dei chatbot standard, questa architettura implementa caching vettoriale e memoria conversazionale, permettendo all'utente di porre domande sequenziali sul documento caricato risparmiando costi API.

(Inserisci qui uno screenshot della tua app una volta avviata)

🏗️ Architettura Tecnica

Il progetto è costruito su uno stack Python moderno e scalabile:

Frontend: Streamlit (Interfaccia Web reattiva)

Orchestration: LangChain (Gestione della logica AI)

Vector Database: FAISS (Indicizzazione vettoriale locale in-memory)

LLM: OpenAI gpt-4o-mini / gpt-3.5-turbo (Modello di linguaggio)

Embedding: OpenAI text-embedding-3-small

⚡ Caratteristiche Principali

Analisi Istantanea: Carica qualsiasi PDF e ottieni risposte basate sui dati in pochi secondi.

Smart Chunking: Il documento viene spezzato in segmenti intelligenti (1500 token) per mantenere il contesto finanziario (es. tabelle e note a piè di pagina).

Performance Caching: Utilizza @st.cache_resource per evitare di ricalcolare gli embedding ad ogni domanda.

Sicurezza: I documenti vengono processati in locale e non vengono salvati permanentemente su nessun server.

🚀 Guida all'Installazione (Da Zero)

Segui questi passaggi per avviare l'applicazione sul tuo computer.

Prerequisiti

Python 3.8+ installato sul tuo sistema.

Una API Key di OpenAI (inizia con sk-...).

1. Clona la Repository

Apri il terminale (o Prompt dei Comandi) e scarica il progetto:

git clone [https://github.com/IL_TUO_USERNAME/financial-rag-streamlit.git](https://github.com/IL_TUO_USERNAME/financial-rag-streamlit.git)
cd financial-rag-streamlit


2. Crea un Ambiente Virtuale (Opzionale ma Consigliato)

Isola le dipendenze del progetto per non creare conflitti:

Su Windows:

python -m venv venv
venv\Scripts\activate


Su Mac/Linux:

python3 -m venv venv
source venv/bin/activate


3. Installa le Dipendenze

Scarica le librerie necessarie (LangChain, Streamlit, FAISS, ecc.):

pip install -r requirements.txt


4. Avvia l'Applicazione

Lancia il server locale di Streamlit:

streamlit run app.py


Appena lanciato il comando, si aprirà automaticamente una scheda nel tuo browser all'indirizzo http://localhost:8501.

📖 Come Usare l'App

Inserisci la API Key: Nella barra laterale a sinistra, incolla la tua chiave OpenAI (sk-...). La chiave non viene salvata.

Configura l'AI: (Opzionale) Seleziona il modello (es. gpt-4o-mini) e la creatività (Temperature).

Carica il PDF: Trascina il tuo bilancio o contratto nell'area di upload.

Chatta: Attendi il messaggio verde "Documento indicizzato!" e inizia a fare domande.

Esempio: "Qual è il fatturato totale del 2024?"

Esempio: "Riassumi i rischi legali citati a pagina 5."

📂 Struttura del Progetto

financial-rag-streamlit/
├── app.py                # Il codice principale dell'applicazione
├── requirements.txt      # Lista delle librerie Python
├── README.md             # Documentazione (questo file)
└── .gitignore            # File da ignorare (per sicurezza)


⚖️ Licenza

Questo progetto è rilasciato sotto licenza MIT. Sentiti libero di usarlo e modificarlo per i tuoi progetti personali o commerciali.

