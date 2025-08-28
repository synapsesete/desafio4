"""
Processador de dados Excel para automação de VR/VA
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class VRDataProcessor:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gpt-4o-mini')
        
        # Inicializar LLM
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0,
            openai_api_key=self.openai_api_key
        )
        
        # Dicionários para armazenar dados
        self.data = {}
        self.final_data = None
        
        # Carregar prompt personalizado
        self.load_custom_prompt()
    
    def load_custom_prompt(self):
        """Carrega o prompt personalizado do arquivo"""
        try:
            prompt_path = os.path.join('data', 'prompt.md')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.custom_prompt = f.read()
            print("Prompt personalizado carregado com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar prompt: {str(e)}")
            self.custom_prompt = ""
    
    def load_excel_files(self):
        """Carrega todos os arquivos Excel necessários"""
        files_to_load = {
            'ativos': 'ATIVOS.xlsx',
            'ferias': 'FÉRIAS.xlsx',
            'desligados': 'DESLIGADOS.xlsx',
            'admissao': 'ADMISSÃOABRIL.xlsx',
            'afastamentos': 'AFASTAMENTOS.xlsx',
            'aprendiz': 'APRENDIZ.xlsx',
            'estagio': 'ESTÁGIO.xlsx',
            'exterior': 'EXTERIOR.xlsx',
            'base_sindicato': 'Basesindicatoxvalor.xlsx',
            'base_dias_uteis': 'Basediasuteis.xlsx',
            'vr_mensal': 'VRMENSAL05.2025.xlsx',
            'vr_final_ref': 'VR_Mensal_05.2025_Final27ago.xlsx'
        }
        
        for key, filename in files_to_load.items():
            try:
                file_path = os.path.join('data', filename)
                
                # Tratamento especial para base_dias_uteis (pular primeira linha)
                if key == 'base_dias_uteis':
                    df = pd.read_excel(file_path, skiprows=1)
                else:
                    df = pd.read_excel(file_path)
                
                self.data[key] = df
                print(f"Arquivo {filename} carregado: {len(df)} registros")
                
                # Mostrar colunas para debug
                print(f"Colunas de {key}: {list(df.columns)}")
                print("---")
                
            except Exception as e:
                print(f"Erro ao carregar {filename}: {str(e)}")
                self.data[key] = pd.DataFrame()
    
    def analyze_data_structure(self):
        """Analisa a estrutura dos dados carregados"""
        print("\\n=== ANÁLISE DA ESTRUTURA DOS DADOS ===\\n")
        
        for key, df in self.data.items():
            if not df.empty:
                print(f"\\n{key.upper()}:")
                print(f"  Registros: {len(df)}")
                print(f"  Colunas: {list(df.columns)}")
                
                # Mostrar algumas linhas de exemplo
                if len(df) > 0:
                    print(f"  Exemplo (primeiras 2 linhas):")
                    print(df.head(2).to_string(index=False))
                print("-" * 50)
    
    def get_eligible_employees(self):
        """Identifica colaboradores elegíveis ao VR"""
        if 'ativos' not in self.data or self.data['ativos'].empty:
            print("Dados de colaboradores ativos não encontrados.")
            return pd.DataFrame()
        
        # Começar com colaboradores ativos
        eligible = self.data['ativos'].copy()
        print(f"Colaboradores ativos iniciais: {len(eligible)}")
        
        # Remover exclusões baseadas em matrícula
        exclusions = []
        
        # Adicionar matrículas de exclusão
        for exclusion_type in ['aprendiz', 'estagio', 'afastamentos', 'exterior']:
            if exclusion_type in self.data and not self.data[exclusion_type].empty:
                df_exclusion = self.data[exclusion_type]
                # Tentar diferentes nomes de coluna para matrícula
                matricula_col = None
                for col in df_exclusion.columns:
                    if 'matricula' in col.lower() or 'matrícula' in col.lower():
                        matricula_col = col
                        break
                
                if matricula_col:
                    exclusions.extend(df_exclusion[matricula_col].tolist())
                    print(f"Exclusões de {exclusion_type}: {len(df_exclusion)} registros")
        
        # Aplicar exclusões
        if exclusions:
            # Encontrar coluna de matrícula nos ativos
            matricula_col_ativos = None
            for col in eligible.columns:
                if 'matricula' in col.lower() or 'matrícula' in col.lower():
                    matricula_col_ativos = col
                    break
            
            if matricula_col_ativos:
                before_exclusion = len(eligible)
                eligible = eligible[~eligible[matricula_col_ativos].isin(exclusions)]
                print(f"Após exclusões: {len(eligible)} (removidos: {before_exclusion - len(eligible)})")
        
        return eligible
    
    def calculate_working_days(self, employee_data):
        """Calcula dias úteis para um colaborador"""
        # Esta é uma implementação simplificada
        # Na versão completa, consideraria sindicato, férias, afastamentos, etc.
        
        # Assumir 22 dias úteis por mês como padrão
        working_days = 22
        
        # Ajustar baseado em dados específicos se disponível
        return working_days
    
    def calculate_vr_values(self, eligible_employees):
        """Calcula valores de VR para colaboradores elegíveis"""
        if eligible_employees.empty:
            return pd.DataFrame()
        
        # Preparar dados para cálculo
        result_data = []
        
        for index, employee in eligible_employees.iterrows():
            # Extrair dados básicos
            matricula = employee.get('MATRICULA', employee.get('Matrícula', 'N/A'))
            nome = employee.get('NOME', employee.get('Nome', 'N/A'))
            sindicato = employee.get('SINDICATO', employee.get('Sindicato', 'PADRÃO'))
            
            # Calcular dias úteis
            dias_uteis = self.calculate_working_days(employee)
            
            # Valor padrão do VR (será ajustado baseado no sindicato)
            valor_vr_diario = 30.00  # Valor exemplo
            
            # Buscar valor específico do sindicato se disponível
            if 'base_sindicato' in self.data and not self.data['base_sindicato'].empty:
                sindicato_data = self.data['base_sindicato']
                sindicato_row = sindicato_data[sindicato_data['SINDICATO'] == sindicato]
                if not sindicato_row.empty:
                    valor_vr_diario = sindicato_row.iloc[0].get('VALOR', valor_vr_diario)
            
            # Calcular valores
            valor_total = dias_uteis * valor_vr_diario
            valor_empresa = valor_total * 0.80  # 80% empresa
            valor_desconto = valor_total * 0.20  # 20% colaborador
            
            result_data.append({
                'Matrícula': matricula,
                'Nome': nome,
                'Sindicato': sindicato,
                'Dias Úteis': dias_uteis,
                'Valor do VR': valor_vr_diario,
                'Valor Total': valor_total,
                'Valor Empresa (80%)': valor_empresa,
                'Valor Descontado (20%)': valor_desconto,
                'Status': 'ATIVO'
            })
        
        return pd.DataFrame(result_data)
    
    def process_data(self):
        """Processa todos os dados e gera planilha final"""
        print("\\n=== INICIANDO PROCESSAMENTO DE DADOS ===\\n")
        
        # Carregar arquivos
        self.load_excel_files()
        
        # Analisar estrutura
        self.analyze_data_structure()
        
        # Obter colaboradores elegíveis
        eligible_employees = self.get_eligible_employees()
        
        if eligible_employees.empty:
            print("Nenhum colaborador elegível encontrado.")
            return None
        
        # Calcular valores de VR
        final_result = self.calculate_vr_values(eligible_employees)
        
        # Salvar resultado
        output_path = os.path.join('output', 'VR_Mensal_05_2025_Gerado.xlsx')
        os.makedirs('output', exist_ok=True)
        
        final_result.to_excel(output_path, index=False)
        print(f"\\nPlanilha final salva em: {output_path}")
        print(f"Total de colaboradores processados: {len(final_result)}")
        
        # Mostrar resumo
        print("\\n=== RESUMO DOS RESULTADOS ===")
        print(final_result.to_string(index=False))
        
        self.final_data = final_result
        return final_result

def main():
    """Função principal"""
    processor = VRDataProcessor()
    result = processor.process_data()
    
    if result is not None:
        print("\\nProcessamento concluído com sucesso!")
        print(f"Modelo LLM utilizado: {processor.model_name}")
    else:
        print("\\nFalha no processamento dos dados.")

if __name__ == "__main__":
    main()

