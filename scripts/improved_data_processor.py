"""
Processador de dados Excel melhorado para automação de VR/VA

Grupo: Synapse 7 - Desafio 4
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

class ImprovedVRDataProcessor:
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
                
            except Exception as e:
                print(f"Erro ao carregar {filename}: {str(e)}")
                self.data[key] = pd.DataFrame()
    
    def find_column(self, df, possible_names):
        """Encontra uma coluna baseada em possíveis nomes"""
        for col in df.columns:
            for name in possible_names:
                if name.lower() in col.lower():
                    return col
        return None
    
    def get_eligible_employees(self):
        """Identifica colaboradores elegíveis ao VR baseado na planilha de referência"""
        # Usar a planilha de referência final como base
        if 'vr_final_ref' not in self.data or self.data['vr_final_ref'].empty:
            print("Planilha de referência final não encontrada.")
            return pd.DataFrame()
        
        ref_data = self.data['vr_final_ref'].copy()
        print(f"Dados de referência carregados: {len(ref_data)} registros")
        
        # Filtrar apenas colaboradores elegíveis
        if 'ELEGIVEL' in ref_data.columns:
            eligible = ref_data[ref_data['ELEGIVEL'] == True].copy()
        elif 'Status' in ref_data.columns:
            eligible = ref_data[ref_data['Status'] == 'Elegível'].copy()
        else:
            # Se não há coluna de elegibilidade, usar todos
            eligible = ref_data.copy()
        
        print(f"Colaboradores elegíveis encontrados: {len(eligible)}")
        return eligible
    
    def get_sindicato_values(self):
        """Obtém valores de VR por sindicato"""
        sindicato_values = {}
        
        if 'base_sindicato' in self.data and not self.data['base_sindicato'].empty:
            sindicato_data = self.data['base_sindicato']
            
            # Encontrar colunas de sindicato e valor
            sindicato_col = self.find_column(sindicato_data, ['sindicato', 'sindic'])
            valor_col = self.find_column(sindicato_data, ['valor', 'vr'])
            
            if sindicato_col and valor_col:
                for _, row in sindicato_data.iterrows():
                    sindicato = row[sindicato_col]
                    valor = row[valor_col]
                    if pd.notna(sindicato) and pd.notna(valor):
                        sindicato_values[sindicato] = float(valor)
                        
                print(f"Valores de sindicato carregados: {len(sindicato_values)}")
            else:
                print("Colunas de sindicato/valor não encontradas na base de sindicatos")
        
        # Valores padrão se não encontrados
        if not sindicato_values:
            sindicato_values = {
                'São Paulo': 37.5,
                'Rio Grande do Sul': 35.0,
                'PADRÃO': 30.0
            }
            print("Usando valores padrão de sindicato")
        
        return sindicato_values
    
    def get_dias_uteis_por_sindicato(self):
        """Obtém dias úteis por sindicato"""
        dias_uteis = {}
        
        if 'base_dias_uteis' in self.data and not self.data['base_dias_uteis'].empty:
            dias_data = self.data['base_dias_uteis']
            
            # Encontrar colunas
            sindicato_col = self.find_column(dias_data, ['sindicato', 'sindic'])
            dias_col = self.find_column(dias_data, ['dias', 'uteis'])
            
            if sindicato_col and dias_col:
                for _, row in dias_data.iterrows():
                    sindicato = row[sindicato_col]
                    dias = row[dias_col]
                    if pd.notna(sindicato) and pd.notna(dias):
                        # Mapear nomes de sindicatos
                        if 'SP' in str(sindicato).upper():
                            dias_uteis['São Paulo'] = int(dias)
                        elif 'RS' in str(sindicato).upper():
                            dias_uteis['Rio Grande do Sul'] = int(dias)
                        else:
                            dias_uteis[str(sindicato)] = int(dias)
                            
                print(f"Dias úteis por sindicato: {dias_uteis}")
            else:
                print("Colunas de dias úteis não encontradas")
        
        # Valores padrão
        if not dias_uteis:
            dias_uteis = {
                'São Paulo': 22,
                'Rio Grande do Sul': 21,
                'PADRÃO': 22
            }
            print("Usando dias úteis padrão")
        
        return dias_uteis
    
    def process_data_with_reference(self):
        """Processa dados usando a planilha de referência como guia"""
        print("\\n=== PROCESSAMENTO BASEADO NA PLANILHA DE REFERÊNCIA ===\\n")
        
        # Carregar arquivos
        self.load_excel_files()
        
        # Obter colaboradores elegíveis da referência
        eligible_employees = self.get_eligible_employees()
        
        if eligible_employees.empty:
            print("Nenhum colaborador elegível encontrado na referência.")
            return None
        
        # Obter valores de sindicato e dias úteis
        sindicato_values = self.get_sindicato_values()
        dias_uteis_sindicato = self.get_dias_uteis_por_sindicato()
        
        # Processar cada colaborador
        result_data = []
        
        for index, employee in eligible_employees.iterrows():
            try:
                # Extrair dados básicos
                matricula = employee.get('MATRICULA', 'N/A')
                
                # Tentar diferentes colunas para nome
                nome = (employee.get('NOME') or 
                       employee.get('Nome') or 
                       employee.get('TITULO DO CARGO', 'N/A'))
                
                # Sindicato mapeado (preferir o mapeado)
                sindicato = (employee.get('Sindicato Mapeado') or 
                           employee.get('Sindicato_y') or 
                           employee.get('Sindicato_x') or 
                           'PADRÃO')
                
                # Dias úteis calculados (usar da referência se disponível)
                if 'DIAS UTEIS CALCULADOS' in employee and pd.notna(employee['DIAS UTEIS CALCULADOS']):
                    dias_uteis = int(employee['DIAS UTEIS CALCULADOS'])
                else:
                    dias_uteis = dias_uteis_sindicato.get(sindicato, 22)
                
                # Valor VR diário (usar da referência se disponível)
                if 'VALOR VR DIARIO' in employee and pd.notna(employee['VALOR VR DIARIO']):
                    valor_vr_diario = float(employee['VALOR VR DIARIO'])
                else:
                    valor_vr_diario = sindicato_values.get(sindicato, 30.0)
                
                # Calcular valores
                valor_total = dias_uteis * valor_vr_diario
                valor_empresa = valor_total * 0.80  # 80% empresa
                valor_desconto = valor_total * 0.20  # 20% colaborador
                
                # Status
                status = employee.get('Status', 'Elegível')
                
                result_data.append({
                    'Matrícula': matricula,
                    'Nome': nome,
                    'Sindicato': sindicato,
                    'Dias Úteis': dias_uteis,
                    'Valor do VR': valor_vr_diario,
                    'Valor Total': valor_total,
                    'Valor Empresa (80%)': valor_empresa,
                    'Valor Descontado (20%)': valor_desconto,
                    'Status': status
                })
                
            except Exception as e:
                print(f"Erro ao processar colaborador {matricula}: {str(e)}")
                continue
        
        # Criar DataFrame final
        final_result = pd.DataFrame(result_data)
        
        # Salvar resultado
        output_path = os.path.join('output', 'VR_Mensal_05_2025_Gerado.xlsx')
        os.makedirs('output', exist_ok=True)
        
        final_result.to_excel(output_path, index=False)
        print(f"\\nPlanilha final salva em: {output_path}")
        print(f"Total de colaboradores processados: {len(final_result)}")
        
        # Calcular totais
        total_valor_empresa = final_result['Valor Empresa (80%)'].sum()
        total_valor_desconto = final_result['Valor Descontado (20%)'].sum()
        total_geral = final_result['Valor Total'].sum()
        
        print(f"\\n=== RESUMO FINANCEIRO ===")
        print(f"Total Valor Empresa (80%): R$ {total_valor_empresa:,.2f}")
        print(f"Total Desconto Colaborador (20%): R$ {total_valor_desconto:,.2f}")
        print(f"Total Geral: R$ {total_geral:,.2f}")
        
        # Mostrar primeiros registros
        print(f"\\n=== PRIMEIROS 10 REGISTROS ===")
        print(final_result.head(10).to_string(index=False))
        
        self.final_data = final_result
        return final_result

def main():
    """Função principal"""
    processor = ImprovedVRDataProcessor()
    result = processor.process_data_with_reference()
    
    if result is not None:
        print("\\nProcessamento concluído com sucesso!")
        print(f"Modelo LLM utilizado: {processor.model_name}")
        
        # Salvar também em formato CSV para facilitar visualização
        csv_path = os.path.join('output', 'VR_Mensal_05_2025_Gerado.csv')
        result.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Arquivo CSV salvo em: {csv_path}")
        
    else:
        print("\\nFalha no processamento dos dados.")

if __name__ == "__main__":
    main()

