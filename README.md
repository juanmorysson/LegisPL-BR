# LegisPL-BR

Conjunto de dados estruturado com proposições legislativas do tipo Projeto de Lei (PL) da Câmara dos Deputados do Brasil, abrangendo os anos de 2022, 2023 e 2024. O repositório inclui o dataset final em formato `.xlsx` e o código Python necessário para coleta, enriquecimento e exportação dos dados, a partir da API pública da Câmara.

---

## 📚 Conteúdo

- `projetos_PL_2022_2024_completo.xlsx`: base final com 1500 proposições legislativas enriquecidas com autores e tramitações
- `tramitacao.py`: script Python modular para coleta e processamento
- `figuras/`: diagramas ilustrativos usados no artigo (fluxo de coleta e etapas do script)
- `README.md`: instruções de uso
- `requirements.txt`: dependências do projeto (pode ser gerado com `pip freeze`)

---

## 🚀 Como usar

### 1. Clonar o repositório

git clone https://github.com/juanmorysson/LegisPL-BR.git
cd LegisPL-BR

### 2. Criar ambiente virtual (opcional, mas recomendado)

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

### 3. Instalar as dependências

pip install -r requirements.txt
Ou, se ainda não tiver o requirements.txt, instale diretamente:

pip install pandas requests openpyxl

### 4. Executar o script

python tramitacao.py

### ⚙️ Personalização do script
Você pode editar a lista de anos e o tipo de proposição diretamente no tramitacao.py:

anos = [2022, 2023, 2024]         # Altere para incluir novos anos
tipo = "PL"                       # Pode ser "PEC", "MPV", etc.
O script usa paginação automática e espaçamento entre chamadas à API para respeitar os limites de acesso público.

### 📦 Formato de saída
O arquivo final .xlsx contém as seguintes colunas:

Coluna	Tipo	Descrição
id	int	Identificador único da proposição na Câmara
tipo	str	Tipo da proposição (ex: PL)
numero	int	Número da proposição no ano
ano	int	Ano de apresentação da proposição
ementa	str	Resumo textual da proposição
autores	str	Lista dos autores separados por vírgula
último_órgão	str	Órgão responsável pela última tramitação
última_tramitação	str	Descrição da última movimentação
data_da_última_tramitação	str	Data da última tramitação (formato YYYY-MM-DD)

### 📄 Licença
Este projeto está licenciado sob a Licença MIT. Você pode usá-lo, copiá-lo e modificá-lo livremente com a devida atribuição.

### 📚 Citação
Se você utilizar este dataset ou o código associado em sua pesquisa, por favor cite o artigo:

Juan Morysson. LegisPL-BR: Um Conjunto de Dados Aberto de Proposições Legislativas da Câmara dos Deputados (2022–2024). In: Dataset Workshop - Simpósio Brasileiro de Banco de Dados (SBBD), 2025.

### 🤝 Contribuições
Sinta-se à vontade para abrir issues, enviar pull requests, ou sugerir melhorias na estrutura do código e expansão do dataset para outros tipos de proposições (ex: PEC, MPV).
