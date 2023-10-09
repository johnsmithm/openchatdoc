import os
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
import uuid, glob, shutil
from dotenv import load_dotenv

load_dotenv()

FILES_DIR = os.environ.get("FILES_DIR")
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

def process_files(files):

    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    text_splitter = CharacterTextSplitter(        
        separator = "\n",
        chunk_size = 2000,
        chunk_overlap  = 100,
        length_function = len,
    )

    for file in files:
        filename = file.filename

        new_file_name = str(uuid.uuid4())

        persist_directory = os.path.join(FILES_DIR, new_file_name)

        os.makedirs(persist_directory)

        file_path = os.path.join(persist_directory, filename)

        file.save(file_path)

        documents = []

        if file_path.split('.')[-1].lower() in ['pdf']:
            pdf_file = open(file_path, 'rb')

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pag = []
            # Loop through all the pages in the PDF file
            for page_num in range(len(pdf_reader.pages)):
                # Get the page object
                page_obj = pdf_reader.pages[page_num]

                # Extract the text from the page
                page_text = page_obj.extract_text()

                documents.append(Document(page_content=page_text, metadata={'source':filename}))
                
        if file_path.split('.')[-1].lower() in ['txt','md','json','xml']:
            loader = TextLoader(file_path)
            documents = loader.load()

        if file_path.split('.')[-1].lower() in ['docx','doc']:
            loader = Docx2txtLoader(file_path)
            documents = loader.load()

        if len(documents)>0:

            texts = text_splitter.split_documents(documents)
          
            if os.path.exists(persist_directory):
                db = FAISS.from_documents(texts, embeddings)
                db.save_local(persist_directory)
                db.save_local(FILES_DIR+'/all')

    if os.path.exists(FILES_DIR+'/all'):
        shutil.rmtree(FILES_DIR+'/all')

    index_files()

def index_files():
    db = None

    for folder in glob.glob(FILES_DIR+'/*'):
        new_db = FAISS.load_local(folder, embeddings)
        if db is None:
            db = new_db
            continue
        db.merge_from(new_db)
    if db is not None:
        db.save_local(FILES_DIR+'/all')
            

def get_context(query):
    if len(glob.glob(FILES_DIR+'/all'))==0:
        return ''
    db = FAISS.load_local(FILES_DIR+'/all', embeddings)

    retriever = db.as_retriever()

    docs = retriever.get_relevant_documents(query)

    context = ''
    for doc in docs:
        context += f'Source:{doc.metadata["source"].split("/")[-1]}\nText:\n{doc.page_content}\n\n'

    return context
