
#  Sicredi Data Pipeline

Um projeto  que implementa uma pipeline de engenharia de dados para análise de inadimplência e perfil de cooperativas de crédito, com base em dados simulados do Sicredi. A estrutura abrange ingestão, tratamento e geração de insights, utilizando Python, Pandas, análises via Jupyter Notebook e Power BI.

---

##  Estrutura do Projeto

```bash
SICREDI_DATA_PIPELINE/
│
├── datalake/                 
│   ├── input/                
│   ├── silver/               
│   └── gold/                 
│
├── scripts/                 
│   └── pipeline_sicredi.py   
│
├── notebooks/
│   └── analise_sicredi.ipynb 
│
├── dashboards/
│   └── sicredi_data_pipeline.pbix
│
├── configs/                  
│
├── requirements.txt          
├── docker-compose.yml        
├── Dockerfile                
├── Makefile                  
├── .env                      
├── .gitignore                
└── README.md                 
```

---

##  Tecnologias Utilizadas

- **Python 3.11**
- **Pandas**
- **Seaborn / Matplotlib**
- **Jupyter Notebook**
- **Power BI**
- **Docker e Docker Compose**
- **Make**

---

##  Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/seuusuario/sicredi_pipeline.git
cd sicredi_pipeline
```

### 2. Criar e ativar o ambiente virtual (opcional)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a pipeline localmente

```bash
python scripts/pipeline_sicredi.py
```

### 5. Rodar com Docker

```bash
docker-compose up --build
```

---

##  Análises Geradas

O dashboard `dashboards/sicredi_data_pipeline.pbix`  utiliza os dados processados para gerar gráficos como: Inadimplência mensal, Inadimplência por cooperativa e Volume da taxa de juros.

O notebook `notebooks/analise_sicredi.ipynb` utiliza os dados sem tratamento e com tratamento para gerar análises como: Distribuição da idade dos associados, Verificação de tipos de dados e a Verificação de dados nulos.

---

##  Estrutura do Datalake

- `input/`: dados simulados brutos
- `silver/`: tabelas relacionais limpas (`dim_associado`, `dim_conta`, `dim_cooperativa`, `fct_operacao_credito`)
- `gold/`: indicadores analíticos prontos (`inadimplencia_mensal`, `inadimplencia_por_cooperativa`, `media_idade_por_faixa`)

---

##  Checklist

- [x] Pipeline funcional com leitura e gravação em CSV
- [x] Dados transformados nas camadas Silver e Gold
- [x] Notebook com análise descritiva
- [x] Dashboard no Power BI com visualizações
- [x] Containerização com Docker
- [x] Reprodutível com Makefile e `requirements.txt`

---

##  Possíveis Melhorias Futuras

- Implementação de testes automatizados
- Suporte a formato Parquet ou Delta Lake
- Integração com bancos de dados relacionais (PostgreSQL, Redshift)
- Deploy em cloud (AWS/GCP/DATABRICKS)

---

##  Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
