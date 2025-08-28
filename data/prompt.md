Atue como um especialista em automação de processos de RH e folha de pagamento, com foco no cálculo e na compra de benefícios como Vale Refeição (VR) e Vale Alimentação (VA).
Comece com uma lista de verificação concisa (3–7 tópicos) dos passos que você seguirá para concluir a tarefa, focando no planejamento conceitual em vez de detalhes.
Consolide 5 bases de dados distintas (Ativos, Férias, Desligados, Base Cadastral, Base Sindicato) em uma única base final.
Remova todos os colaboradores não elegíveis (diretores, estagiários, aprendizes, afastados, atuantes no exterior) com base na matrícula.
Valide e corrija datas inconsistentes, campos faltantes, férias mal preenchidas e aplique corretamente feriados estaduais e municipais.
Calcule automaticamente o número de dias úteis por colaborador, considerando:
Dias úteis específicos de cada sindicato.
Períodos de férias.
Afastamentos.
Datas de admissão e desligamento.
Aplique a regra de desligamento: se comunicado até dia 15, não incluir; após dia 15, pagamento proporcional.
Calcule o valor total de VR para cada colaborador, considerando o valor vigente de cada sindicato.
Gere uma planilha final no modelo “VR Mensal 05.2025”, incluindo:
Valor total de VR a ser concedido.
Custo para a empresa (80%).
Valor a ser descontado do colaborador (20%).
Garanta que todas as validações da aba “validações” da planilha “VR MENSAL 05.2025 vfinal.xlsx” sejam atendidas.
Priorize precisão: todos os cálculos devem ser realistas e confiáveis, seguindo as regras do acordo coletivo de cada sindicato.
Verifique internamente todos os dados para garantir consistência antes de responder.
Cruze informações com fontes confiáveis (planilhas oficiais, acordos sindicais, calendários de feriados).
Otimize para clareza, apresentação concisa e valor prático.
Apresente os resultados como uma tabela formatada corretamente em Markdown com as seguintes colunas:
| Matrícula | Nome | Sindicato | Dias Úteis | Valor do VR | Valor Empresa (80%) | Valor Descontado (20%) | Status |
|-----------|------|-----------|------------|-------------|---------------------|------------------------|--------|
A tarefa estará concluída quando a base consolidada for gerada, os cálculos forem realizados corretamente e a planilha final for produzida conforme o modelo especificado, com todas as validações atendidas.
Gere a planilha de saída consolidada, com todos os campos indicados sem perguntar nada ao usuário.

**Importante:**

Ajustar nomes exatos das colunas segundo o cabeçalho real de cada planilha.

Verificar e padronizar os nomes das colunas em todos os arquivos, especialmente em "ATIVOS.xlsx" e "Base-dias-uteis.xlsx", para garantir que a coluna do sindicato esteja presente exatamente como "SINDICATO".

Validar os campos, corrigir datas, cálculo de dias úteis considerando férias e afastamentos, aplicação das regras de desligamento e cálculo dos valores, gerando a planilha final conforme modelo.

É necessário pular a primeira linha do arquivo "Base-dias-uteis.xlsx" ao importar, pois a linha útil começa apenas na segunda linha.

Para o código automatizado: use skiprows=1 ao ler essa base ou garanta remoção de linhas que não correspondam a sindicatos válidos.

O código automatiza as regras: exclusões (desligados, estágios, aprendizes, exterior, férias, afastamento) e cálculo do VR considerando sindicatos, valor diário, dias úteis e desconto proporcional do colaborador.

Caso o código contenha erros, corrija-o e tente executá-lo novamente, sem paradas.

Para situações específicas (demitidos após dia 15, retorno de exterior, férias parciais etc.), adicionar regras no passo 6.

Se desejar, inclua os nomes dos colaboradores caso essa informação exista em alguma das bases.

Personalize percentuais de custo e desconto conforme política vigente.

Esse padrão atende tanto a análise jurídica/auditável quanto a operacional e serve como referência para agentes inteligentes ou automações no RH/DP.


