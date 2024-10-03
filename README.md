
---

# Clash Royale Analysis - MongoDB

Este projeto tem como objetivo realizar uma consultas detalhadas de dados de batalhas do jogo **Clash Royale**, utilizando **MongoDB** como banco de dados NoSQL para armazenamento de dados. As análises incluem consultas para identificar cartas mais usadas, jogadores com alta frequência de vitórias, entre outras métricas que ajudam a balancear o jogo.

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```
ClashRoyaleAnalysis-MongoDB/
│
├──__pycache__
│   └── db.cpython-312.pyc
|
├── data/
│   ├── BattlesStaging_01042021_WL_tagged.txt  # Dados brutos das batalhas
│   └── cardid_and_name.csv          # Dados de mapeamento de IDs das cartas com seus nomes
│
├── query1.py                    # Consulta 1: Jogadores que usaram uma carta específica
├── query2.py                    # Consulta 2: Cartas mais utilizadas em vitórias
├── query3.py                    # Consulta 3: Cartas mais utilizadas em derrotas
├── query4.py                    # Consulta 4: Análise de decks vencedores
├── query5.py                    # Consulta 5: Análise de cartas mais populares
├── query6.py                    # Consulta 6: Jogadores com maior taxa de vitórias
├── query7.py                    # Consulta 7: Jogadores com maior uso de uma carta específica
├── query8.py                    # Consulta 8: Análise comparativa de cartas usadas
├── dashboard.py                # Dashboard interativo desenvolvido em Streamlit
├── create_df_and_import_data.py     # Script para criar DataFrames e importar dados para o MongoDB
├── db.py                            # Conexão e manipulação de dados no MongoDB
├── README.md                        # Documentação do projeto
├── .gitignore                       # Arquivo Gitignore
├── .gitattributes                   # Atributos do Git
├── requirements.txt                 # Dependências do projeto (bibliotecas)
```

## Funcionalidades

- **Análise de Batalhas**: O projeto realiza a análise das batalhas para identificar padrões no uso de cartas, vitórias e derrotas.
- **MongoDB**: Utilizado para armazenar os dados das batalhas e permitir consultas eficientes.
- **Dashboard Interativo**: Desenvolvido com **Streamlit**, permite a visualização das análises geradas de forma intuitiva.
- **Consultas Analíticas**: Scripts em Python para realizar consultas diretamente no banco de dados MongoDB, focando em diferentes aspectos como jogadores, cartas e decks.

## Como Executar

### Pré-requisitos

- **Python 3.9+**
- **MongoDB**
- **Docker** (opcional, caso deseje rodar o MongoDB em container)
- Instale as dependências do projeto com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Instruções de Uso

1. **Importe os dados**:
   - Utilize o script `create_df_and_import_data.py` para converter os arquivos de dados (`BattlesStaging_01042021_WL_tagged.txt` e `cardid_and_name.csv`) em DataFrames e importar os dados para o MongoDB.

2. **Execute as consultas**:
   - Navegue até o diretório `querys_consultas` e execute os scripts desejados para realizar as análises.
   - Por exemplo, para executar a **Consulta 1**, utilize o comando:

   ```bash
   python query1.py
   ```

3. **Dashboard**:
   - Para visualizar o dashboard interativo, execute o seguinte comando no diretório `dashboard`:

   ```bash
   streamlit run dashboard.py
   ```

   O dashboard permitirá a seleção de datas e cartas para visualizar as análises em tempo real.

## Dependências

As principais dependências do projeto estão listadas no arquivo `requirements.txt`:

- `matplotlib==3.9.2`: Biblioteca para criação de gráficos e visualizações.
- `pandas==2.2.3`: Utilizado para manipulação de dados em DataFrames.
- `pymongo==4.10.1`: Interface para comunicação com o banco de dados MongoDB.
- `streamlit==1.39.0`: Framework para construção de aplicações web interativas e dashboards.

## Contribuindo

Fique à vontade para contribuir com este projeto enviando pull requests ou sugerindo melhorias através de issues.

---