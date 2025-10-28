import networkx as nx
import matplotlib.pyplot as plt
import json
from matplotlib.lines import Line2D
import re
import numpy as np

NODE_DISTANCE = 1.2

# with open("../texts_result/relations_ver2.json", "r", encoding="utf-8") as f:
with open("../texts_result/relations.json", "r", encoding="utf-8") as f:

    relations = json.load(f)


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


relation_colors = {
    "co-occurrence": "#8ecae6",
    "metaphoric": "#ffb703",
    "emotional_association": "#fb8500",
}

cluster_colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

G = nx.Graph()
merge_map = {}

for rel in relations:
    n1, n2 = normalize(rel["node1"]), normalize(rel["node2"])
    merge_map[rel["node1"]] = n1
    merge_map[rel["node2"]] = n2
    color = relation_colors.get(rel["relation_type"], "gray")
    label = rel.get("symbolic_layer", "")
    G.add_edge(n1, n2, label=label, color=color)

connected_components = [c for c in nx.connected_components(G) if len(c) >= 3]
filtered_nodes = set().union(*connected_components)
G_filtered = G.subgraph(filtered_nodes)
components = list(nx.connected_components(G_filtered))

node_cluster_colors = {}
for i, component in enumerate(components):
    color = cluster_colors[i % len(cluster_colors)]
    for node in component:
        node_cluster_colors[node] = color


def improved_layout(G, k=1.2, iterations=200):
    pos = nx.spring_layout(G, k=k, iterations=iterations, threshold=1e-4, seed=42, scale=2)
    return optimize_layout(G, pos, additional_iterations=100)


def optimize_layout(G, pos, additional_iterations=100):
    nodes = list(G.nodes())
    edges = list(G.edges())
    pos = pos.copy()

    for iteration in range(additional_iterations):
        total_force = {node: np.array([0.0, 0.0]) for node in nodes}

        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i >= j:
                    continue
                x1, y1 = pos[node1]
                x2, y2 = pos[node2]
                dx, dy = x1 - x2, y1 - y2
                distance = max(np.sqrt(dx * dx + dy * dy), 0.1)

                repulsion_force = 2.0 / (distance * distance) if distance < 0.5 else 0.5 / (distance * distance)
                total_force[node1] += np.array([dx / distance * repulsion_force, dy / distance * repulsion_force])
                total_force[node2] -= np.array([dx / distance * repulsion_force, dy / distance * repulsion_force])

        for u, v in edges:
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            dx, dy = x1 - x2, y1 - y2
            distance = max(np.sqrt(dx * dx + dy * dy), 0.1)

            attraction_force = distance * 0.3
            total_force[u] -= np.array([dx / distance * attraction_force, dy / distance * attraction_force])
            total_force[v] += np.array([dx / distance * attraction_force, dy / distance * attraction_force])

        damping = 0.1 * (1 - iteration / additional_iterations)
        for node in nodes:
            force_magnitude = np.sqrt(total_force[node][0] ** 2 + total_force[node][1] ** 2)
            if force_magnitude > 0.3:
                total_force[node] = total_force[node] / force_magnitude * 0.3
            pos[node] = (pos[node][0] + total_force[node][0] * damping,
                         pos[node][1] + total_force[node][1] * damping)

    return pos


def separate_clusters_layout(G, components, horizontal_spacing=3.0, vertical_spacing=2.0):
    """
    Розділяє кластери по сітці, зберігаючи їх внутрішнє розташування
    """
    # Спочатку отримуємо гарне розташування для всього графа
    base_pos = improved_layout(G, k=NODE_DISTANCE, iterations=200)

    # Для кожного кластера знаходимо його центр та розміри
    cluster_data = []
    for cluster in components:
        cluster_nodes = list(cluster)

        # Знаходимо bounding box кластера
        x_coords = [base_pos[node][0] for node in cluster_nodes]
        y_coords = [base_pos[node][1] for node in cluster_nodes]

        center_x = (max(x_coords) + min(x_coords)) / 2
        center_y = (max(y_coords) + min(y_coords)) / 2
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)

        cluster_data.append({
            'nodes': cluster_nodes,
            'center': (center_x, center_y),
            'width': width,
            'height': height,
            'original_pos': {node: base_pos[node] for node in cluster_nodes}
        })

    # Сортуємо кластери за кількістю вузлів (найбільші перші)
    cluster_data.sort(key=lambda x: len(x['nodes']), reverse=True)

    # Розташовуємо кластери по сітці
    separated_pos = {}
    cols = int(np.ceil(np.sqrt(len(components))))
    rows = int(np.ceil(len(components) / cols))

    for i, cluster in enumerate(cluster_data):
        row = i // cols
        col = i % cols

        # Центр нового положення кластера
        new_center_x = col * horizontal_spacing
        new_center_y = row * vertical_spacing

        # Обчислюємо зсув
        old_center_x, old_center_y = cluster['center']
        shift_x = new_center_x - old_center_x
        shift_y = new_center_y - old_center_y

        # Зсуваємо всі вузли кластера
        for node in cluster['nodes']:
            old_x, old_y = cluster['original_pos'][node]
            separated_pos[node] = (old_x + shift_x, old_y + shift_y)

    return separated_pos


def adjust_positions_for_labels(pos, G, min_distance=0.4):
    pos_new = pos.copy()
    nodes = list(G.nodes())

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            node1, node2 = nodes[i], nodes[j]
            x1, y1 = pos_new[node1]
            x2, y2 = pos_new[node2]
            dx, dy = x1 - x2, y1 - y2
            distance = np.sqrt(dx * dx + dy * dy)

            if distance < min_distance:
                if abs(dx) < 0.01 and abs(dy) < 0.01:
                    dx, dy = 0.1, 0.1
                    distance = np.sqrt(dx * dx + dy * dy)

                factor = (min_distance - distance) / distance
                move_x, move_y = dx * factor * 0.3, dy * factor * 0.3
                pos_new[node1] = (x1 + move_x, y1 + move_y)
                pos_new[node2] = (x2 - move_x, y2 - move_y)

    return pos_new


# Використовуємо розділене розташування кластерів
pos = separate_clusters_layout(G_filtered, components, horizontal_spacing=4.0, vertical_spacing=3.0)
pos = adjust_positions_for_labels(pos, G_filtered)

node_degrees = dict(G_filtered.degree())
node_colors_list = [node_cluster_colors[n] for n in G_filtered.nodes()]
node_sizes = [300 + node_degrees[n] * 40 for n in G_filtered.nodes()]
edge_colors = [G_filtered[u][v]["color"] for u, v in G_filtered.edges()]

plt.figure(figsize=(20, 16))  # Трохи збільшимо розмір для кращого відображення

# Малюємо спочатку ребра, потім вузли
nx.draw_networkx_edges(G_filtered, pos, alpha=0.6, edge_color=edge_colors, width=1.2)
nx.draw_networkx_nodes(G_filtered, pos, node_color=node_colors_list, node_size=node_sizes,
                       edgecolors='black', linewidths=0.6, alpha=0.9)

# Мітки вузлів
node_labels = {}
for node in G_filtered.nodes():
    if len(node) > 25:
        words = node.split()
        shortened = ""
        for word in words:
            if len(shortened + word) <= 22:
                shortened += word + " "
            else:
                break
        node_labels[node] = shortened.strip() + "..."
    elif len(node) > 20:
        node_labels[node] = node[:18] + "..."
    else:
        node_labels[node] = node

nx.draw_networkx_labels(G_filtered, pos, labels=node_labels, font_size=7, font_weight='bold',
                        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.3'))

# Мітки ребер
edge_labels = nx.get_edge_attributes(G_filtered, "label")
formatted_edge_labels = {}
for edge, label in edge_labels.items():
    label_str = str(label)
    if len(label_str) > 20:
        words = label_str.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + word) <= 15:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
                if len(lines) >= 2:
                    break
        if current_line and len(lines) < 3:
            lines.append(current_line.strip())
        formatted_edge_labels[edge] = "\n".join(lines)
    elif len(label_str) > 10:
        words = label_str.split()
        if len(words) > 1:
            mid = len(words) // 2
            formatted_edge_labels[edge] = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])
        else:
            formatted_edge_labels[edge] = label_str
    else:
        formatted_edge_labels[edge] = label_str

# Малюємо мітки ребер з кращим позиціонуванням
if formatted_edge_labels:
    nx.draw_networkx_edge_labels(G_filtered, pos, edge_labels=formatted_edge_labels,
                                 font_size=5, font_color="dimgray",
                                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none',
                                           boxstyle='round,pad=0.2'))

# Легенда
relation_legend = [Line2D([0], [0], color=color, lw=2, label=typ) for typ, color in relation_colors.items()]
cluster_legend = [Line2D([0], [0], marker='o', color='w', label=f'Кластер {i + 1} ({len(comp)} вузлів)',
                         markerfacecolor=cluster_colors[i % len(cluster_colors)], markersize=8)
                  for i, comp in enumerate(components[:8])]

plt.legend(handles=relation_legend + cluster_legend, title="Легенда карти",
           loc="center left", frameon=True, bbox_to_anchor=(1, 0.5))

plt.axis('off')
plt.tight_layout()
plt.subplots_adjust(right=0.85)
plt.show()

print(f"Загальна кількість кластерів: {len(components)}")
print(f"Загальна кількість вузлів: {G_filtered.number_of_nodes()}")
print(f"Загальна кількість ребер: {G_filtered.number_of_edges()}")
for i, comp in enumerate(components[:5]):
    print(f"Кластер {i + 1}: {len(comp)} вузлів")