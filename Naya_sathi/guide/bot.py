from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_together import Together
from langchain.prompts import PromptTemplate
import google.generativeai as genai

class LegalAssistant:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.qa_chain = None
        self.vectorstore = None
        self._initialize_components()
        
    def _initialize_components(self):
        # Step 1: Load PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        # Step 2: Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Step 3: Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False}
        )

        # Step 4: Create vector store
        self.vectorstore = FAISS.from_documents(texts, embeddings)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        # Step 5: Custom prompt
        prompt_template = """Use the following pieces of context to provide a thorough answer.
        If you don't know, just say you don't know.

        Context: {context}

        Question: {question}

        Provide a comprehensive answer:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # Step 6: Configure LLM (API key hardcoded - NOT RECOMMENDED)
        llm = Together(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
            together_api_key="442f97a9bf348a0486f931a5c86538c273ba620dc9c75e8c138545acec7c6859"  # INSECURE
        )

        # Step 7: Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT},
            verbose=True
        )

        # Step 8: Configure Gemini (API key hardcoded - NOT RECOMMENDED)
        genai.configure(api_key="AIzaSyDPoolssaQEiKq8q0qqDEC5oV16t5pgjsk")  # INSECURE

    def get_response(self, query):
        # Get initial response
        response = self.qa_chain({"query": query})
        ans = response["result"]
        
        # Simplify with Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        simplified_response = model.generate_content(
            f"Simplify and add more context relevant to Nepal: {ans}"
        )
        
        return {
            "original_response": ans,
            "simplified_response": simplified_response.text,
            "source_documents": response["source_documents"]
        }
