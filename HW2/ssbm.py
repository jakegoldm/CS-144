import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

n = 30
k = 3
A = 0.7
B = 0.1

seed = 3

random.seed(seed)
np.random.seed(seed)

G = nx.Graph()
for i in range(n):
    G.add_node(i)
communities = np.random.randint(0, k, n)

for i in range(n): 
    for j in range(i + 1, n): 
        if communities[i] == communities[j]: 
            prob = random.choices([0, 1], weights=[1 - A, A])[0]
        else: 
            prob = random.choices([0, 1], weights=[1 - B, B])[0]
        if prob: 
            G.add_edge(i, j)

# Figure 1: Original Drawing
plt.figure(figsize=(12, 6))
colors = ["blue", "red", "green", "orange", "purple", "yellow"]
color_map = [colors[communities[i]] for i in range(n)]
nx.draw(G, node_color=color_map, with_labels=True)
plt.title('Original Drawing')
plt.savefig("HW2/imgs/ssbm_spring.png")

# Figure 2: Kamada-Kawai Layout
plt.figure(figsize=(12, 6))
pos = nx.kamada_kawai_layout(G)
nx.draw(G, pos=pos, node_color=color_map, with_labels=True, edge_color="grey")
plt.title('Kamada-Kawai Layout')
plt.savefig("HW2/imgs/ssbm_kk.png")
