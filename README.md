# Sistema de Automação de VR/VA com Langchain

Este projeto implementa um sistema automatizado para processamento de dados de Vale Refeição (VR) e Vale Alimentação (VA) utilizando Langchain, Python e técnicas de RAG (Retrieval-Augmented Generation).

## 📋 Descrição

O sistema processa múltiplas planilhas Excel contendo dados de colaboradores, aplica regras de negócio específicas e gera uma planilha final com os valores de VR a serem concedidos, considerando:

- Colaboradores elegíveis (excluindo diretores, estagiários, aprendizes, afastados, etc.)
- Dias úteis por sindicato
- Valores específicos por sindicato
- Regras de desligamento
- Cálculo de custos (80% empresa, 20% colaborador)

## 🏗️ Arquitetura

### Componentes Principais

1. **Sistema RAG (`rag_system.py`)**
   - Carrega e processa o PDF de contexto
   - Cria embeddings e vectorstore com FAISS
   - Permite consultas inteligentes sobre as regras de negócio

2. **Processador de Dados (`improved_data_processor.py`)**
   - Carrega e processa arquivos Excel
   - Aplica regras de elegibilidade
   - Calcula valores de VR
   - Gera planilha final

3. **Aplicação Principal (`main_application.py`)**
   - Integra RAG e processamento de dados
   - Interface para execução e consultas

## 📁 Projeto:

```
├── data/                          # Dados de entrada
│   ├── ATIVOS.xlsx               # Colaboradores ativos
│   ├── FÉRIAS.xlsx               # Dados de férias
│   ├── DESLIGADOS.xlsx           # Colaboradores desligados
│   ├── ADMISSÃOABRIL.xlsx        # Admissões de abril
│   ├── AFASTAMENTOS.xlsx         # Afastamentos
│   ├── APRENDIZ.xlsx             # Aprendizes
│   ├── ESTÁGIO.xlsx              # Estagiários
│   ├── EXTERIOR.xlsx             # Colaboradores no exterior
│   ├── Basesindicatoxvalor.xlsx  # Valores por sindicato
│   ├── Basediasuteis.xlsx        # Dias úteis por sindicato
│   ├── VRMENSAL05.2025.xlsx      # Dados mensais VR
│   ├── Desafio4-Descrição.pdf    # Contexto RAG
│   └── prompt.md                 # Prompt personalizado
├── scripts/                      # Scripts Python
│   ├── rag_system.py            # Sistema RAG
│   ├── improved_data_processor.py # Processador de dados
│   └── main_application.py      # Aplicação principal
├── output/                       # Arquivos gerados
│   ├── VR_Mensal_05_2025_Gerado.xlsx
│   └── VR_Mensal_05_2025_Gerado.csv
├── .env                         # Variáveis de ambiente
├── requirements.txt             # Dependências
└── README.md                    # Este arquivo
```

## 🚀 Instalação e Uso

### Pré-requisitos

- Python 3.11+
- Chave de API OpenAI configurada

### Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   OPENAI_API_KEY=chave
   OPENAI_API_BASE=https://api.openai.com/v1
   MODEL_NAME=gpt-4o-mini
   ```

### Execução

Execute a aplicação principal:
```bash
python scripts/main_application.py
```

Ou execute componentes individuais:
```bash
# Apenas processamento de dados
python scripts/improved_data_processor.py

# Apenas sistema RAG
python scripts/rag_system.py
```

## 📊 Resultados

O sistema processa **1.794 colaboradores elegíveis** e gera:

### Estatísticas Finais
- **Total de colaboradores processados**: 1.794
- **Valor total de VR**: R$ 1.321.320,00
- **Custo para empresa (80%)**: R$ 1.057.056,00
- **Desconto dos colaboradores (20%)**: R$ 264.264,00

### Arquivos Gerados
- `output/VR_Mensal_05_2025_Gerado.xlsx` - Planilha Excel final
- `output/VR_Mensal_05_2025_Gerado.csv` - Arquivo CSV para análise

### Formato da Planilha Final

| Matrícula | Nome | Sindicato | Dias Úteis | Valor do VR | Valor Total | Valor Empresa (80%) | Valor Descontado (20%) | Status |
|-----------|------|-----------|------------|-------------|-------------|---------------------|------------------------|--------|
| 34941 | TECH RECRUITER II | São Paulo | 22 | 37.5 | 825.0 | 660.0 | 165.0 | Elegível |
| 24401 | COORDENADOR ADMINISTRATIVO | Rio Grande do Sul | 21 | 35.0 | 735.0 | 588.0 | 147.0 | Elegível |

## 🤖 Modelo LLM Utilizado

**Modelo**: `gpt-4o-mini`

## 🔧 Funcionalidades Técnicas

### Sistema RAG
- **Embeddings**: OpenAI Embeddings
- **Vectorstore**: FAISS

### Processamento de Dados
- **Leitura**: pandas + openpyxl
- **Cálculos**: Dias úteis, valores por sindicato
- **Saída**: Excel e CSV

### Regras de Negócio Implementadas
1. **Exclusões automáticas**:
   - Diretores
   - Estagiários
   - Aprendizes
   - Afastados
   - Colaboradores no exterior

2. **Cálculo de dias úteis**:
   - Por sindicato específico
   - Considerando férias e afastamentos
   - Regras de desligamento (até dia 15)

3. **Valores por sindicato**:
   - São Paulo: R$ 37,50/dia
   - Rio Grande do Sul: R$ 35,00/dia
   - Outros: valores específicos

4. **Divisão de custos**:
   - Empresa: 80%
   - Colaborador: 20%



## Autores - Grupo Synapse 7:

- [Adriana Rocha Castro de Paula] (adrianarcdepaula@gmail.com)
- [Conrado Gornic](cgornic@gmail.com)
- [Lia Yumi Morimoro](yumi.lia.mori@gmail.com)
- [Luiz Fernando Rezende](rio2040@gmail.com)
- [Rodrigo Mibielli Peixoto](rodrigo.mibielli@gmail.com)
- [Saulo Brotto](haredo.i@gmail.com)

