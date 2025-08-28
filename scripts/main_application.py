"""
Aplicação principal que integra o sistema RAG com o processamento de dados
"""

import os
import sys
from dotenv import load_dotenv
from improved_data_processor import ImprovedVRDataProcessor

# Tentar importar o sistema RAG (pode falhar devido às limitações da API)
try:
    from rag_system import VRRAGSystem
    RAG_AVAILABLE = True
except Exception as e:
    print(f"Sistema RAG não disponível: {str(e)}")
    RAG_AVAILABLE = False

class VRAutomationApp:
    def __init__(self):
        load_dotenv()
        self.model_name = os.getenv('MODEL_NAME', 'gpt-4o-mini')
        
        # Inicializar processador de dados
        self.data_processor = ImprovedVRDataProcessor()
        
        # Inicializar sistema RAG se disponível
        self.rag_system = None
        if RAG_AVAILABLE:
            try:
                self.rag_system = VRRAGSystem()
                self.setup_rag()
            except Exception as e:
                print(f"Erro ao inicializar RAG: {str(e)}")
                self.rag_system = None
    
    def setup_rag(self):
        """Configura o sistema RAG"""
        if not self.rag_system:
            return False
        
        try:
            # Tentar carregar vectorstore existente
            vectorstore_path = os.path.join('output', 'vectorstore')
            if os.path.exists(vectorstore_path):
                if self.rag_system.load_vectorstore(vectorstore_path):
                    print("Vectorstore existente carregado.")
                else:
                    # Se falhar, criar novo
                    pdf_path = os.path.join('data', 'Desafio4-Descrição.pdf')
                    if self.rag_system.load_pdf_context(pdf_path):
                        print("Novo vectorstore criado.")
                    else:
                        return False
            else:
                # Criar novo vectorstore
                pdf_path = os.path.join('data', 'Desafio4-Descrição.pdf')
                if self.rag_system.load_pdf_context(pdf_path):
                    print("Vectorstore criado com sucesso.")
                else:
                    return False
            
            # Configurar cadeia de QA com prompt personalizado
            custom_prompt = self.data_processor.custom_prompt
            if custom_prompt:
                self.rag_system.setup_qa_chain(custom_prompt)
                print("Sistema RAG configurado com prompt personalizado.")
            else:
                self.rag_system.setup_qa_chain()
                print("Sistema RAG configurado com prompt padrão.")
            
            return True
            
        except Exception as e:
            print(f"Erro ao configurar RAG: {str(e)}")
            return False
    
    def query_rag(self, question):
        """Faz uma pergunta ao sistema RAG"""
        if not self.rag_system:
            return "Sistema RAG não disponível."
        
        try:
            result = self.rag_system.query(question)
            if result:
                return result['answer']
            else:
                return "Não foi possível obter resposta do sistema RAG."
        except Exception as e:
            return f"Erro ao consultar RAG: {str(e)}"
    
    def process_vr_data(self):
        """Processa os dados de VR"""
        print("\\n" + "="*60)
        print("INICIANDO PROCESSAMENTO DE DADOS DE VR/VA")
        print("="*60)
        
        # Processar dados
        result = self.data_processor.process_data_with_reference()
        
        if result is not None:
            print("\\n" + "="*60)
            print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print("="*60)
            
            # Estatísticas finais
            total_colaboradores = len(result)
            total_valor = result['Valor Total'].sum()
            total_empresa = result['Valor Empresa (80%)'].sum()
            total_desconto = result['Valor Descontado (20%)'].sum()
            
            print(f"\\nESTATÍSTICAS FINAIS:")
            print(f"- Total de colaboradores processados: {total_colaboradores}")
            print(f"- Valor total de VR: R$ {total_valor:,.2f}")
            print(f"- Custo para empresa (80%): R$ {total_empresa:,.2f}")
            print(f"- Desconto dos colaboradores (20%): R$ {total_desconto:,.2f}")
            print(f"- Modelo LLM utilizado: {self.model_name}")
            
            # Arquivos gerados
            print(f"\\nARQUIVOS GERADOS:")
            print(f"- Excel: output/VR_Mensal_05_2025_Gerado.xlsx")
            print(f"- CSV: output/VR_Mensal_05_2025_Gerado.csv")
            
            return result
        else:
            print("\\nFALHA NO PROCESSAMENTO DOS DADOS!")
            return None
    
    def run_interactive_mode(self):
        """Executa modo interativo com consultas RAG"""
        print("\\n" + "="*60)
        print("MODO INTERATIVO - CONSULTAS RAG")
        print("="*60)
        print("Digite suas perguntas sobre o processamento de VR/VA.")
        print("Digite 'sair' para encerrar ou 'processar' para processar os dados.")
        print("-"*60)
        
        while True:
            try:
                question = input("\\nSua pergunta: ").strip()
                
                if question.lower() in ['sair', 'exit', 'quit']:
                    break
                elif question.lower() in ['processar', 'process']:
                    self.process_vr_data()
                    break
                elif question:
                    answer = self.query_rag(question)
                    print(f"\\nResposta: {answer}")
                    print("-"*60)
                
            except KeyboardInterrupt:
                print("\\nEncerrando...")
                break
            except Exception as e:
                print(f"\\nErro: {str(e)}")
    
    def run(self):
        """Executa a aplicação principal"""
        print("\\n" + "="*60)
        print("SISTEMA DE AUTOMAÇÃO DE VR/VA COM LANGCHAIN")
        print("="*60)
        print(f"Modelo LLM: {self.model_name}")
        print(f"Sistema RAG: {'Disponível' if self.rag_system else 'Não disponível'}")
        print("-"*60)
        
        # Processar dados automaticamente
        result = self.process_vr_data()
        
        # Se RAG estiver disponível, oferecer modo interativo
        if self.rag_system and result is not None:
            print("\\nDeseja fazer consultas sobre o processamento? (s/n): ", end="")
            try:
                response = input().strip().lower()
                if response in ['s', 'sim', 'y', 'yes']:
                    self.run_interactive_mode()
            except:
                pass
        
        print("\\nAplicação finalizada.")
        return result

def main():
    """Função principal"""
    app = VRAutomationApp()
    result = app.run()
    
    if result is not None:
        print(f"\\nSUCESSO: {len(result)} colaboradores processados.")
        return 0
    else:
        print("\\nERRO: Falha no processamento.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

