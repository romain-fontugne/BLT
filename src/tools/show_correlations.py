import networkx as nx
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import pandas as pd

graph = nx.Graph()
correlations = pd.DataFrame()

f = open("correlation.txt", "r")
for line in f:
    if "#" in line:
        node_name = line.split()
        node_name.pop(0)
    else:
        corr = line.split()
        correlations = correlations.append(pd.DataFrame([corr]))
correlations.columns = node_name
correlations.index = node_name
for nodey in node_name:
    for nodex in node_name:
        correlation = float(correlations.ix[nodey, nodex])
        if abs(correlation) > 0.3 and abs(correlation) != 1:
            if nodex not in graph.nodes():
                graph.add_node(nodex)
            if nodey not in graph.nodes():
                graph.add_node(nodey)
            if (nodex, nodey) not in graph.edges() or (nodey, nodex) not in graph.edges():
                graph.add_edge(nodex, nodey, weight=correlation)

edge_width = [ d["weight"]*5 for (u,v,d) in graph.edges(data=True)]
pos = nx.spring_layout(graph, k=0.77)
nx.draw_networkx(graph, pos, width = edge_width)
plt.axis("off")
plt.savefig("correlation_graph.png")
