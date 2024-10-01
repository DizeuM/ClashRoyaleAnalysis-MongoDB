import pandas as pd
from typing import Optional 
from db import conectar_banco

# Conecta ao banco de dados
client = conectar_banco()

if client:
    try:
        # Carrega o arquivo CSV contendo os dados das batalhas
        df: Optional[pd.DataFrame] = pd.read_csv('./data/BattlesStaging_01042021_WL_tagged.csv')
        print("Arquivo .csv carregado com sucesso!")
    except Exception as e:
        # Em caso de erro, imprime a exceção e define df como None
        print(e)
        df = None

    if df is not None:
        # Seleciona apenas as colunas relevantes do DataFrame
        df = df[['battleTime', 'winner.tag', 'winner.startingTrophies', 'winner.trophyChange', 'winner.crowns', 
                 'winner.card1.id', 'winner.card2.id', 'winner.card3.id', 'winner.card4.id', 'winner.card5.id', 
                 'winner.card6.id', 'winner.card7.id', 'winner.card8.id', 
                 'loser.tag', 'loser.startingTrophies', 'loser.trophyChange', 'loser.crowns', 
                 'loser.card1.id', 'loser.card2.id', 'loser.card3.id', 'loser.card4.id', 'loser.card5.id', 
                 'loser.card6.id', 'loser.card7.id', 'loser.card8.id', 'arena.id']]

        
        def criar_deck(row, tipo_jogador):
            return [row[f'{tipo_jogador}.card{i}.id'] for i in range(1, 9)]

        # Função para organizar os dados de uma batalha em um dicionário
        def organizar_batalha(row):
            return {
                "battle_time": row['battleTime'],
                "winner": {
                    "nickname": row['winner.tag'],
                    "starting_trophies": row['winner.startingTrophies'],
                    "trophy_change": row['winner.trophyChange'],
                    "crowns": row['winner.crowns'],
                    "deck": criar_deck(row, 'winner')
                },
                "loser": {
                    "nickname": row['loser.tag'],
                    "starting_trophies": row['loser.startingTrophies'],
                    "trophy_change": row['loser.trophyChange'],
                    "crowns": row['loser.crowns'],
                    "deck": criar_deck(row, 'loser')
                },
                "arena": row['arena.id']
            }

        # Aplica a função de organização de batalha a cada linha do DataFrame
        batalhas = df.apply(organizar_batalha, axis=1)

        # Conecta ao banco de dados e insere os dados das batalhas
        db = client['clash_royale']
        batalhas_collection = db['batalhas']
        batalhas_collection.insert_many(batalhas.tolist())

        print("Banco criado e dados inseridos com sucesso!")
    else:
        print("Falha ao carregar o arquivo .csv.")
