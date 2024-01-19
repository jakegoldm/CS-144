import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Load CSV into a Pandas DataFrame
df = pd.read_csv("HW2/network.csv")

# Create a directed graph from the DataFrame
G: nx.Graph = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

# Calculate outdegree and indegree for each node
outdegrees = dict(G.out_degree())
indegrees = dict(G.in_degree())

# Plot histograms
plt.figure(figsize=(12, 6))

# Outdegree histogram
plt.subplot(1, 2, 1)
plt.hist(outdegrees.values(), bins=range(0, 250, 10), color='blue', edgecolor='black')
plt.title('Outdegree')
plt.xlabel('Outdegree')
plt.ylabel('Frequency')
plt.xlim(0, 250)
plt.ylim(0, 1000)

# Indegree histogram
plt.subplot(1, 2, 2)
plt.hist(indegrees.values(), bins=range(0, 250, 10), color='green', edgecolor='black')
plt.title('Indegree')
plt.xlabel('Indegree')
plt.ylabel('Frequency')
plt.xlim(0, 250)
plt.ylim(0, 1000)

plt.tight_layout()
# plt.show()
plt.savefig("HW2/imgs/histogram.png")

# G_u = G.to_undirected()

# max_diameter = nx.diameter(G_u)
# avg_diameter = nx.average_shortest_path_length(G_u)

# print(f"Max diameter: {max_diameter}")
# print(f"Avg diameter: {avg_diameter}")
