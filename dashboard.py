from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from pymongo import MongoClient

# Função para conectar ao banco de dados MongoDB Atlas
def conectar_banco(connection_string):
    client = MongoClient(connection_string)
    return client

# Conecta ao banco de dados MongoDB Atlas
connection_string = ""
client = conectar_banco(connection_string)
db = client['clash_royale']
batalhas_collection = db['batalhas']

# Função para calcular a porcentagem de vitórias com uma carta específica
def calcular_vitorias_por_carta(carta_id, start_time, end_time):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    total_batalhas = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str}
    })

    vitorias_com_carta = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "winner.deck": carta_id
    })

    return (vitorias_com_carta / total_batalhas * 100) if total_batalhas > 0 else 0

# Função para listar decks com mais de 90% de vitórias
def listar_decks_com_vitorias(min_porcentagem, min_vitorias, start_time, end_time):
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S%z')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S%z')

    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$group": {"_id": "$winner.deck", "total_vitorias": {"$sum": 1}}},
        {"$match": {"total_vitorias": {"$gte": min_vitorias}}},
        {"$project": {
            "_id": 1,
            "total_vitorias": 1,
            "porcentagem_vitorias": {
                "$multiply": [
                    {"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]},
                    100
                ]
            }
        }},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}
    ]
    
    return list(batalhas_collection.aggregate(pipeline, allowDiskUse=True))

# Função para calcular derrotas com um combo de cartas específico
def calcular_derrotas_por_combo(combo_cartas, start_time, end_time):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Filtro para derrotas em batalhas onde o deck adversário contém todas as cartas do combo
    derrotas_com_combo = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "loser.deck": {"$all": combo_cartas}
    })

    return derrotas_com_combo

# Interface do Streamlit
st.sidebar.header("Parâmetros de Análise")

# Entrada do ID da Carta
carta_id = st.sidebar.number_input('ID da Carta', min_value=26000000, step=1, value=26000000)

# Entrada dos IDs das Cartas para Combo (separados por vírgula)
combo_ids_input = st.sidebar.text_input('IDs das Cartas para Combo (separados por vírgula)', '26000001,26000002,26000010')
combo_ids = [int(x) for x in combo_ids_input.split(',')]

# Slider para a porcentagem mínima de vitórias
min_porcentagem_vitorias = st.sidebar.slider('Porcentagem Mínima de Vitórias', 0.0, 100.0, 66.57)

# Entrada do número mínimo de vitórias
min_vitorias = st.sidebar.number_input('Vitórias Mínimas', min_value=1, step=1, value=750)

# Entrada para o período de análise
start_time = st.sidebar.date_input('Data de Início', datetime(2021, 1, 1))
end_time = st.sidebar.date_input('Data de Fim', datetime(2021, 12, 31))

# Título principal
st.title("Dashboard de Análise de Batalhas - Clash Royale")

# Exibe a porcentagem de vitórias com a carta específica
porcentagem_vitorias = calcular_vitorias_por_carta(carta_id, start_time, end_time)
st.subheader(f"Análise de Vitórias com a Carta {carta_id}")
st.write(f"Porcentagem de vitórias com a carta {carta_id}: {porcentagem_vitorias:.2f}%")

# Gráfico de vitórias por carta
fig, ax = plt.subplots()
ax.bar([str(carta_id)], [porcentagem_vitorias])
ax.set_ylabel('Porcentagem de Vitórias')
ax.set_title('Gráfico de Vitórias por Carta')
st.pyplot(fig)

# Query 2: Decks com mais de 90% de vitórias
decks = listar_decks_com_vitorias(min_porcentagem_vitorias, min_vitorias, start_time, end_time)

st.subheader(f"Decks com mais de {min_porcentagem_vitorias}% de vitórias:")
for deck in decks:
    st.write(f"Deck ID: {deck['_id']}, Total de Vitórias: {deck['total_vitorias']}, Porcentagem de Vitórias: {deck['porcentagem_vitorias']:.2f}%")

# Gráfico de decks
if decks:
    deck_ids = [str(deck['_id']) for deck in decks]  # Convertemos os IDs para string para o gráfico
    total_vitorias = [deck['total_vitorias'] for deck in decks]

    fig_decks, ax_decks = plt.subplots()
    ax_decks.bar(deck_ids, total_vitorias, color='lightblue')
    ax_decks.set_xlabel('Deck IDs')
    ax_decks.set_ylabel('Total de Vitórias')
    ax_decks.set_title(f'Distribuição de Vitórias dos Decks com mais de {min_porcentagem_vitorias}%')
    st.pyplot(fig_decks)
else:
    st.write(f"Nenhum deck encontrado com mais de {min_porcentagem_vitorias}% de vitórias.")

# Query 3: Quantidade de derrotas com o combo de cartas
derrotas_combo = calcular_derrotas_por_combo(combo_ids, start_time, end_time)
st.subheader(f"Total de derrotas com o combo de cartas {combo_ids}: {derrotas_combo}")

# Gráfico de derrotas com o combo de cartas
fig_derrotas, ax_derrotas = plt.subplots()
ax_derrotas.plot([derrotas_combo], 'o-r')  # Gráfico de derrota com estilo do exemplo
ax_derrotas.set_ylabel('Total de Derrotas')
ax_derrotas.set_title(f'Gráfico de Derrotas com o Combo {combo_ids}')
st.pyplot(fig_derrotas)

# Função para agrupar cartas perdedoras e contar suas derrotas
def cartas_associadas_a_derrotas(start_time, end_time, limite=10):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Agrupa todas as cartas em decks perdedores e conta a frequência de cada carta
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$unwind": "$loser.deck"},
        {"$group": {"_id": "$loser.deck", "total_derrotas": {"$sum": 1}}},
        {"$sort": {"total_derrotas": -1}},
        {"$limit": limite}
    ]
    
    resultado = list(batalhas_collection.aggregate(pipeline))
    
    return resultado

# Define o período fixo de análise (de 01/01/2021 até 31/12/2023)
start_time = datetime(2021, 1, 1)
end_time = datetime(2023, 12, 31)

# Define o número máximo de cartas a listar
limite = st.sidebar.slider('Número máximo de cartas a listar', min_value=1, max_value=20, value=10)

# Consulta as cartas associadas a derrotas
cartas_derrotas = cartas_associadas_a_derrotas(start_time, end_time, limite)

# Exibe os resultados
st.title("Cartas mais associadas a derrotas")
if cartas_derrotas:
    st.write(f"Período de análise: {start_time} a {end_time}")
    
    # Organiza os dados para o gráfico
    cartas = [str(carta['_id']) for carta in cartas_derrotas]
    total_derrotas = [carta['total_derrotas'] for carta in cartas_derrotas]

    # Cria o gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(cartas, total_derrotas, color='red')
    ax.set_xlabel('ID da Carta')
    ax.set_ylabel('Total de Derrotas')
    ax.set_title('Cartas mais Associadas a Derrotas')
    
    # Rotaciona os IDs das cartas no eixo X para 90 graus
    plt.xticks(rotation=90)
    
    # Exibe o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Nenhuma carta encontrada no período selecionado.")