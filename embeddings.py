from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader

DB_FAISS_PATH = "vectorstore/db_faiss"
loader = CSVLoader(file_path="./data/cleanTripLisbon.csv", encoding="utf-8", csv_args={'delimiter': ','})
data = loader.load()

text_splitter = CharacterTextSplitter(separator='\n')
text_chunks = text_splitter.split_documents(data)

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

docsearch = FAISS.from_documents(text_chunks, embeddings)
docsearch.save_local(DB_FAISS_PATH)