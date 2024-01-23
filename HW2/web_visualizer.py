import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("HW2/network.csv")

df100 = df[(df["source"] <= 100) & (df["target"] <= 100)]
df300 = df[(df["source"] <= 300) & (df["target"] <= 300)]

G100: nx.Graph = nx.from_pandas_edgelist(df100, 'source', 'target', create_using=nx.DiGraph)
G300: nx.Graph = nx.from_pandas_edgelist(df300, 'source', 'target', create_using=nx.DiGraph)

node_degrees = dict(G100.degree())
node_colors = [node_degrees[node] for node in G100.nodes()]
cmap = plt.colormaps.get_cmap("cool")
norm = plt.Normalize(min(node_colors), max(node_colors))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

plt.figure(figsize=(18, 8))
nx.draw(G100, pos=nx.circular_layout(G100), with_labels=True, width=0.3, node_color=node_colors, cmap=cmap)
plt.savefig("HW2/imgs/web100_circle.png")

plt.clf()
nx.draw(G100, pos=nx.kamada_kawai_layout(G100), width=0.3, node_color=node_colors, cmap=cmap)
plt.savefig("HW2/imgs/web100_kk.png")

node_degrees = dict(G300.degree())
node_colors = [node_degrees[node] for node in G300.nodes()]
cmap = plt.colormaps.get_cmap("cool")
norm = plt.Normalize(min(node_colors), max(node_colors))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.clf()
nx.draw(G300, pos=nx.kamada_kawai_layout(G300), width=0.3, node_color=node_colors, cmap=cmap)
plt.savefig("HW2/imgs/web300_kk.png")

plt.clf()
nx.draw(G300, pos=nx.layout.spring_layout(G300, k=2), width=0.3, node_color=node_colors, cmap=cmap)
plt.savefig("HW2/imgs/web300_spring.png")