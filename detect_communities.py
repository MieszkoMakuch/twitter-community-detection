import igraph
import datetime
import sys
import os

prev_date = datetime.datetime.now()

def time_print(text):
    global prev_date
    actual_date = datetime.datetime.now()
    print(f'{(actual_date - prev_date).total_seconds()}: {text}')
    prev_date = actual_date


def plot(g, clusters):
    time_print('Ploting...')

    import numpy as np
    visual_style = {}

    time_print('Scale vertices based on degree')
    outdegree = g.outdegree()
    visual_style["vertex_size"] = [x / max(outdegree) * 25 + 5 for x in outdegree]

    time_print('Set bbox and margin')
    visual_style["bbox"] = (1400, 1400)
    visual_style["margin"] = 100

    time_print('Define colors used for outdegree visualization')
    colours = ['#fecc5c', '#a31a1c']

    time_print('Order vertices in bins based on outdegree')
    bins = np.linspace(0, max(outdegree), len(colours))
    digitized_degrees = np.digitize(outdegree, bins)

    time_print('Set colors according to bins')
    g.vs["color"] = [colours[x - 1] for x in digitized_degrees]

    time_print('Also color the edges')
    for ind, color in enumerate(g.vs["color"]):
        edges = g.es.select(_source=ind)
        edges["color"] = [color]

    time_print('Dont curve the edges')
    visual_style["edge_curved"] = False
    visual_style["vertex_label"] = None

    time_print('Community detection')

    time_print('Set edge weights based on communities')
    weights = {v: len(c) for c in clusters for v in c}
    g.es["weight"] = [weights[e.tuple[0]] + weights[e.tuple[1]] for e in g.es]

    time_print('Choose the layout')
    N = len(g.vs)
    visual_style["layout"] = g.layout_fruchterman_reingold(weights=g.es["weight"], maxiter=1000, area=N ** 3,
                                                           repulserad=N ** 3)
    time_print('Plot the graph')
    out = igraph.plot(g, **visual_style)
    out.save(f'data/{sys.argv[1]}_{sys.argv[2]}.png')


def find_communities_fastgreedy(g):
    time_print('Finding communities "fastgreedy"...')
    communities = g.community_fastgreedy()
    time_print('Finding clusters "fastgreedy"...')
    clusters = communities.as_clustering()
    return clusters


def find_communities_edge_betweenness(g):
    # TODO nie wiem czy się zawiesza czy działa bardzo długo
    return
    time_print('Finding communities "edge betweenness"...')
    communities = g.community_edge_betweenness()
    time_print('Finding clusters "edge betweenness"...')
    clusters = communities.as_clustering()
    return clusters


def find_communities_walktrap(g):
    time_print('Finding communities "walktrap"...')
    communities = g.community_walktrap()
    time_print('Finding clusters "walktrap"...')
    clusters = communities.as_clustering()
    return clusters

    
def find_communities_eigenvector(g):
    time_print('Finding communities "eigenvector"...')
    clusters = g.community_leading_eigenvector()
    return clusters


def find_communities_spinglass(g):
    # TODO split into connected parts
    return


def find_communities_label_propagation(g):
    time_print('Finding communities "label propagation"...')
    clusters = g.community_label_propagation()
    return clusters


def find_communities_multilevel(g):
    time_print('Finding communities "multilevel"...')
    clusters = g.community_multilevel()
    return clusters


def find_communities_infomap(g):
    time_print('Finding communities "infomap"...')
    clusters = g.community_infomap()
    return clusters


def find_communities_optimal_modularity(g):
    # TODO GLPK not implemented ???
    return
    time_print('Finding communities "optimal modularity"...')
    communities = g.community_optimal_modularity()
    time_print('Finding clusters "optimal modularity"...')
    clusters = communities.as_clustering()
    return clusters


def main():
    if not os.path.isfile(sys.argv[1]):
        print('First argument must be name of existing file with model')
        return
        
    time_print('Loading graph...')
    g = igraph.read(sys.argv[1])
    alg = sys.argv[2]
    if alg == 'fg':
        fg = find_communities_fastgreedy(g)
        plot(g, fg)
    elif alg == 'eb':
        eb = find_communities_edge_betweenness(g)
        plot(eb)
    elif alg == 'w':
        w = find_communities_walktrap(g)
        plot(w)
    elif alg == 'ew':
        ew = find_communities_eigenvector(g)
        plot(ew)
    elif alg == 's':
        s = find_communities_spinglass(g)
        plot(s)
    elif alg == 'lp':
        lp = find_communities_label_propagation(g)
        plot(lp)
    elif alg == 'ml':
        ml = find_communities_multilevel(g)
        plot(ml)
    elif alg == 'im':
        im = find_communities_infomap(g)
        plot(im)
    elif alg == 'om':
        om = find_communities_optimal_modularity(g)
        plot(om)
    else:
        print('Incorrect second argument. Must be one of [fg, eb, w, ew, s, lp, ml, im, om]')
        return


if __name__ == '__main__':
    main()




# def main():
#     import csv
#     from fa2 import ForceAtlas2
    
#     if not os.path.isfile(TMP_GRAPH_FILENAME):
#         G, nodes = build_graph()
#         time_print('Saving networkx graph...')
#         nx.write_gml(G, TMP_GRAPH_FILENAME)
    
#     time_print('Reading networkx graph into igraph...')
#     G = ig.Graph()
#     G = G.Read_GML(TMP_GRAPH_FILENAME)
    
#     forceatlas2 = ForceAtlas2(
#                         # Behavior alternatives
#                         outboundAttractionDistribution=True,  # Dissuade hubs
#                         linLogMode=False,  # NOT IMPLEMENTED
#                         adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
#                         edgeWeightInfluence=1.0,

#                         # Performance
#                         jitterTolerance=1.0,  # Tolerance
#                         barnesHutOptimize=True,
#                         barnesHutTheta=1.2,
#                         multiThreaded=False,  # NOT IMPLEMENTED

#                         # Tuning
#                         scalingRatio=2.0,
#                         strongGravityMode=False,
#                         gravity=1.0,

#                         # Log
#                         verbose=True)
    
 
        
#     # calculate dendrogram
#     time_print('communities')
#     communities = G.community_infomap()
    
    
    
#     layout = forceatlas2.forceatlas2_igraph_layout(G, pos=None, iterations=100)
#     ig.plot(communities, layout=layout)
#     # convert it into a flat clustering
#     # time_print('clusters')
#     #clusters = dendrogram.as_clustering()
    
#     #ig.plot.layout.forceatlas2(g, iterations=10000, plotstep=500)
    
#     time_print('plotting')
#     #ig.plot(communities)
#     time_print('finish')
#     return
        
        
#     with open('twitter_network.csv', 'r') as edges_csv:
#         reader = csv.reader(edges_csv)
#         next(reader)  # skip header
#         edges = []
#         for i, row in enumerate(reader):
#             if i % 1000 == 0:
#                 time_print('Adding row numer: ' + str(i))
            
#             edges.append(tuple(row))

#         time_print('Returning edges, size: ' + str(len(edges)))
#         G = ig.Graph.TupleList(edges, directed=False)
    

#     # calculate dendrogram
#     time_print('dendrogram')
#     dendrogram = G.community_fastgreedy()
#     # convert it into a flat clustering
#     time_print('clusters')
#     clusters = dendrogram.as_clustering()
#     # get the membership vector
#     time_print('membership')
#     membership = clusters.membership


 
    
#     print(list(G.vs))

#     time_print(f'Saving igraph to...')
#     with open("output.csv", "w") as output:
#         writer = csv.writer(output)
#         for name, membership in zip(G.vs["name"], membership):
#             writer.writerow([name, membership])

#     #graph_community_fun().write_gml(filename)
#     #save_community_detection_in_gephi_format(G.community_edge_betweenness, 'edge_betweenness.gml')
#     return 0
    
#     save_community_detection_in_gephi_format(G.community_fastgreedy, 'fastgreedy')
#     save_community_detection_in_gephi_format(G.community_infomap, 'infomap')
#     save_community_detection_in_gephi_format(G.community_leading_eigenvector_naive, 'leading_eigenvector_naive')
#     save_community_detection_in_gephi_format(G.community_leading_eigenvector, 'leading_eigenvector')
#     save_community_detection_in_gephi_format(G.community_label_propagation, 'label_propagation')
#     save_community_detection_in_gephi_format(G.community_multilevel, 'multilevel')
#     save_community_detection_in_gephi_format(G.community_optimal_modularity, 'optimal_modularity')
#     save_community_detection_in_gephi_format(G.community_spinglass, 'spinglass')
#     save_community_detection_in_gephi_format(G.community_walktrap, 'walktrap')

    
#     input("Press Enter to continue...")
#     return 0

#     time_print('Moving to numpy matrix...')
#     A = nx.to_numpy_matrix(G)
#     time_print('Creating dataframes...')
#     df = pd.DataFrame(A, index=nodes, columns=nodes)
#     time_print('Saving graph...')
#     df.to_csv('graph.csv', index=True)
#     time_print('Finished...')
