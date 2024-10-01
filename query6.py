# Análise de Cartas Mais Usadas em Combinações Vencedoras
from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def cartas_mais_usadas_em_vitorias(start_time, end_time, limite=10):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Agrupa todas as cartas em decks vencedores e conta a frequência de cada carta
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$unwind": "$winner.deck"},
        {"$group": {"_id": "$winner.deck", "total_usos": {"$sum": 1}}},
        {"$sort": {"total_usos": -1}},
        {"$limit": limite}
    ]
    
    resultado = list(batalhas_collection.aggregate(pipeline))
    
    return resultado

# Exibe as cartas mais usadas em decks vencedores
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)
limite = 10  # Define o número máximo de cartas a listar
cartas_usadas = cartas_mais_usadas_em_vitorias(start_time, end_time, limite)

print("Cartas mais usadas em decks vencedores:")
for carta in cartas_usadas:
    print(f"Carta ID {carta['_id']}: {carta['total_usos']} usos")