import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Load CSV into a Pandas DataFrame
df = pd.read_csv("HW2/network.csv")

G: nx.Graph = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph)

outdegrees = dict(G.out_degree())
indegrees = dict(G.in_degree())

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
plt.savefig("HW2/imgs/histogram.png")

G_u: nx.Graph = G.to_undirected()

print("Computing Diameter...")

max_diameter = nx.diameter(G_u)
avg_diameter = nx.average_shortest_path_length(G_u)

print(f"Max diameter: {max_diameter}")
print(f"Avg diameter: {avg_diameter}")

print("Computing Clustering coefficients...")

triangles_per_vertex = nx.triangles(G_u)
num_triangles = int(sum(triangles_per_vertex.values()) / 3)
counted_triplets = set()

for x in G_u.nodes: 
    for y in G_u.neighbors(x): 
        for z in G_u.neighbors(y):
            if x != z:
                triplet = (x, y, z)
                if (z, y, x) not in counted_triplets: 
                    counted_triplets.add(triplet)

triplets = len(counted_triplets)

print(f"num triangles: {num_triangles}")
print(f"num triplets: {triplets}")

clustering = 3 * num_triangles / triplets
avg_clustering = nx.average_clustering(G_u)

print(f"Clustering Coefficient: {clustering}")
print(f"Avg Clustering Coefficient: {avg_clustering}")

print("Computing ccdfs...")

out_degree_values = np.array(list(outdegrees.values()))
in_degree_values = np.array(list(indegrees.values()))

out_degree_ccdf = 1 - np.cumsum(np.bincount(out_degree_values)[1:]) / G.number_of_nodes()
in_degree_ccdf = 1 - np.cumsum(np.bincount(in_degree_values)[1:]) / G.number_of_nodes()

plt.clf()
plt.loglog(np.arange(1, len(out_degree_ccdf) + 1), out_degree_ccdf, label='Out-degree CCDF')
plt.loglog(np.arange(1, len(in_degree_ccdf) + 1), in_degree_ccdf, label='In-degree CCDF')
plt.xlabel('Degree')
plt.ylabel('Complementary Cumulative Distribution Function (CCDF)')
plt.legend()
plt.savefig("HW2/imgs/ccdf.png")

fp = open("HW2/output_data.txt", "w")
fp.write(f"Max diameter: {max_diameter}\n")
fp.write(f"Avg diameter: {avg_diameter}\n")
fp.write(f"Clustering Coefficient: {clustering}\n")
fp.write(f"Avg Clustering Coefficient: {avg_clustering}\n")
