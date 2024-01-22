import networkx as nx
import random
import matplotlib.pyplot as plt

N = 40
P = 0.23

G = nx.Graph()
for i in range(N): 
    G.add_node(i)

num_possible_edges = int(N * (N - 1) / 2)
edge_probs = random.choices([0, 1], weights=[1 - P, P], k=num_possible_edges)
for i in range(N): 
    for j in range(i + 1, N): 
        if edge_probs.pop(): 
            G.add_edge(i, j)

plt.figure(figsize=(12, 6))
pos_circular = nx.circular_layout(G)
nx.draw(G, pos=pos_circular, with_labels=True, node_color='skyblue', \
        font_color='black', font_size=8, node_size=200, edge_color='gray', \
            font_weight='bold')
plt.title('Erdős-Rényi Circular Layout')
plt.savefig("HW2/imgs/erdos_renyi_circular.png")
plt.clf()

plt.figure(figsize=(12, 6))
pos_spring = nx.spring_layout(G)
nx.draw(G, pos=pos_spring, with_labels=True, node_color='lightcoral', \
        font_color='black', font_size=8, node_size=200, font_weight='bold')
plt.title('Erdős-Rényi Spring Layout')
plt.savefig("HW2/imgs/erdos_renyi_spring.png")
