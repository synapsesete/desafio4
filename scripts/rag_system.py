"""
Sistema RAG (Retrieval-Augmented Generation) para automação de VR/VA
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class VRRAGSystem:
    def __init__(self):
        # Carregar variáveis de ambiente
        load_dotenv()
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gpt-4o-mini')
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 1000))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 200))
        
        # Inicializar componentes
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        
        self.vectorstore = None
        self.qa_chain = None
        
    def load_pdf_context(self, pdf_path):
        """Carrega e processa o PDF para o contexto RAG"""
        try:
            # Carregar PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # Dividir em chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            texts = text_splitter.split_documents(documents)
            
            # Criar vectorstore
            self.vectorstore = FAISS.from_documents(texts, self.embeddings)
            
            # Salvar vectorstore
            vectorstore_path = os.path.join(os.path.dirname(pdf_path), '..', 'output', 'vectorstore')
            os.makedirs(vectorstore_path, exist_ok=True)
            self.vectorstore.save_local(vectorstore_path)
            
            print(f"PDF processado com sucesso. {len(texts)} chunks criados.")
            return True
            
        except Exception as e:
            print(f"Erro ao processar PDF: {str(e)}")
            return False
    
    def load_vectorstore(self, vectorstore_path):
        """Carrega vectorstore existente"""
        try:
            self.vectorstore = FAISS.load_local(vectorstore_path, self.embeddings)
            print("Vectorstore carregado com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao carregar vectorstore: {str(e)}")
            return False
    
    def setup_qa_chain(self, custom_prompt=None):
        """Configura a cadeia de QA com prompt personalizado"""
        if not self.vectorstore:
            raise ValueError("Vectorstore não foi carregado. Execute load_pdf_context() primeiro.")
        
        # Prompt padrão se não fornecido
        if not custom_prompt:
            custom_prompt = """
            Você é um especialista em automação de processos de RH e folha de pagamento, com foco no cálculo e na compra de benefícios como Vale Refeição (VR) e Vale Alimentação (VA).
            
            Use o contexto fornecido para responder às perguntas sobre o processamento de dados de VR/VA.
            
            Contexto: {context}
            
            Pergunta: {question}
            
            Resposta:
            """
        
        prompt = PromptTemplate(
            template=custom_prompt,
            input_variables=["context", "question"]
        )
        
        # Criar cadeia de QA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        print("Cadeia de QA configurada com sucesso.")
    
    def query(self, question):
        """Faz uma pergunta ao sistema RAG"""
        if not self.qa_chain:
            raise ValueError("Cadeia de QA não foi configurada. Execute setup_qa_chain() primeiro.")
        
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            print(f"Erro ao processar pergunta: {str(e)}")
            return None

def main():
    """Função principal para testar o sistema RAG"""
    rag_system = VRRAGSystem()
    
    # Caminho para o PDF
    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Desafio4-Descrição.pdf')
    
    # Carregar PDF e criar vectorstore
    if rag_system.load_pdf_context(pdf_path):
        # Configurar cadeia de QA
        rag_system.setup_qa_chain()
        
        # Teste
        test_question = "Quais são as regras para desligamento de colaboradores no cálculo do VR?"
        result = rag_system.query(test_question)
        
        if result:
            print(f"\nPergunta: {test_question}")
            print(f"Resposta: {result['answer']}")
            print(f"Documentos fonte: {len(result['source_documents'])}")

if __name__ == "__main__":
    main()

