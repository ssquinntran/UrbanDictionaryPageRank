import pickle
import networkx as nx
import matplotlib.pyplot as plt

fread = open("medium_demo_filtered_out", "r+")
fread1 = open("medium_demo_sorted_dict", "r+")
fread2 = open("medium_demo_word_related", "r+")

filtered_out = pickle.load(fread)
sorted_dict = pickle.load(fread1)
word_related = pickle.load(fread2)

fread.close()
fread1.close()
fread2.close()
#print sorted_dict
#print word_related

#find total number of visits
total_visits = sum(sorted_dict.values())
#make a directed graph
G = nx.DiGraph()
#add nodes
#table = []

for k, v in word_related.items():
	if k not in v:
		G.add_node(k)
	for related in v:
		if related in sorted_dict.keys():
			#w = (sorted_dict[related]/float(total_visits))*(1/float(len(v)))
			w = sorted_dict[related]/float(total_visits)
			G.add_edge(k, related, weight=w)
			#table.append((w, k, related))

for a, b, data in sorted(G.edges(data=True), key=lambda (a, b, data): data['weight']):
    #if a == "bushwacked":
    print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))
#pos=nx.random_layout(G) # positions for all nodes

# nodes
#nx.draw_networkx_nodes(G,pos,node_size=700)

# edges
#nx.draw_networkx_edges(G,pos,edgelist=edges, width=1, \
#	alpha=0.5,edge_color='b')

# labels
#nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')

#plt.axis('off')
#plt.savefig("medium_demo_weighted_graph.png") # save as png
#plt.show() # display

#A = nx.adjacency_matrix(G)
#print(A.todense())