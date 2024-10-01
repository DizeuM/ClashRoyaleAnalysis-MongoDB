from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def criar_pipeline(min_porcentagem, min_vitorias, start_time_str, end_time_str, tamanho_combo):
    return [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$group": {
            "_id": {"$slice": ["$winner.deck", tamanho_combo]},  # Agrupa pelo combo de cartas
            "total_vitorias": {"$sum": 1}
        }},
        {"$match": {"total_vitorias": {"$gte": min_vitorias}}},  # Filtra combos com vitórias mínimas
        {"$project": {
            "_id": 1,
            "total_vitorias": 1,
            "porcentagem_vitorias": {
                "$multiply": [
                    {"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]},  # Calcula a porcentagem
                    100
                ]
            }
        }},
        {"$unwind": "$vencedor.deck"},
        {"$group": {
            "_id": {
                "deck": "$vencedor.deck",
                "battleId": "$_id"  # Usando battleId para contar apenas batalhas únicas
            }
        }},
        {"$group": {
            "_id": "$_id.deck",
            "total_batalhas": {"$sum": 1},
            "vitorias": {"$sum": {"$cond": [{ "$eq": ["$winner.tag", "$winner.tag"] }, 1, 0]}},
        }},
        {"$project": {
            "porcentagem_vitorias": {
                "$multiply": [{"$divide": ["$vitorias", "$total_batalhas"]}, 100]
            },
            "deck": "$_id",
            "total_batalhas": 1,
            "vitorias": 1
        }},
        {"$match": {
            "porcentagem_vitorias": {"$gte": porcentagem_vitorias}
        }},
        {"$sort": {
            "porcentagem_vitorias": -1
        }},
        {"$limit": 10}  # Limite opcional para os resultados
    ]

    # Log intermediário
    resultados = list(batalhas_collection.aggregate(pipeline))
    print("Resultados do pipeline:", resultados)  # Adicione esta linha para ver os resultados intermediários

    return resultados

# Definindo parâmetros para a consulta
tamanho_combo = 8  # Defina o tamanho do combo desejado
porcentagem_vitorias = 60  # Porcentagem mínima de vitórias
start_time = datetime(2021, 1, 1)  # Data de início
end_time = datetime(2021, 12, 31)  # Data de fim

# Executando a função e imprimindo os resultados
resultados = combos_cartas_vitoriosos(tamanho_combo, porcentagem_vitorias, start_time, end_time)  # type: ignore # noqa: F821

if resultados:
    print("Combos de cartas que produziram mais de Y% de vitórias:")
    for resultado in resultados:
        print(f"Deck: {resultado['deck']}, Total de Batalhas: {resultado['total_batalhas']}, "
              f"Vitórias: {resultado['vitorias']}, Porcentagem de Vitórias: {resultado['porcentagem_vitorias']:.2f}%")
else:
    print("Nenhum combo de cartas encontrado com as condições especificadas.")
