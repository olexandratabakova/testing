import json
import networkx as nx
import matplotlib.pyplot as plt

# Читаємо JSON з файлу
with open("../texts_result/relations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Створюємо граф
G = nx.Graph()

# Додаємо ребра з атрибутами
for entry in data:
    G.add_edge(
        entry["person1"],
        entry["person2"],
        relation_type=entry["relation_type"],
        polarity=entry["polarity"]
    )

# Розташування вузлів
pos = nx.planar_layout(G, scale=1, center=None, dim=2)

# Малюємо вузли і підписи
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos,
    with_labels=True,
    node_color='lightblue',
    node_size=300,
    font_size=10,
    font_weight='bold',
    edge_color='gray'
)

# Підписи на ребрах
edge_labels = {
    (u, v): f"{d['relation_type']} ({d['polarity']})"
    for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title("Візуалізація зв'язків між особами", fontsize=14, fontweight='bold')
plt.axis('off')
plt.show()
