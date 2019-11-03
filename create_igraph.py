import csv

import logging
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def plot_graph(g):  # TODO - does not work with large graphs (>10k ver)
    import numpy as np
    visual_style = {}

    logging.info('Scale vertices based on degree')
    outdegree = g.outdegree()
    visual_style["vertex_size"] = [x / max(outdegree) * 25 + 5 for x in outdegree]

    logging.info('Set bbox and margin')
    visual_style["bbox"] = (1400, 1400)
    visual_style["margin"] = 100

    logging.info('Define colors used for outdegree visualization')
    colours = ['#fecc5c', '#a31a1c']

    logging.info('Order vertices in bins based on outdegree')
    bins = np.linspace(0, max(outdegree), len(colours))
    digitized_degrees = np.digitize(outdegree, bins)

    logging.info('Set colors according to bins')
    g.vs["color"] = [colours[x - 1] for x in digitized_degrees]

    logging.info('Also color the edges')
    for ind, color in enumerate(g.vs["color"]):
        edges = g.es.select(_source=ind)
        edges["color"] = [color]

    logging.info('Dont curve the edges')
    visual_style["edge_curved"] = False

    logging.info('Community detection')
    communities = g.community_edge_betweenness(directed=True)
    clusters = communities.as_clustering()

    logging.info('Set edge weights based on communities')
    weights = {v: len(c) for c in clusters for v in c}
    g.es["weight"] = [weights[e.tuple[0]] + weights[e.tuple[1]] for e in g.es]

    logging.info('Choose the layout')
    N = len(g.vs)
    visual_style["layout"] = g.layout_fruchterman_reingold(weights=g.es["weight"], maxiter=1000, area=N ** 3,
                                                           repulserad=N ** 3)

    logging.info('Plot the graph')
    plot(g, **visual_style)


def load_edges():
    # loads edge list from csv file
    with open('twitter_network-1k.csv', 'r') as edges_csv:
        reader = csv.reader(edges_csv)
        next(reader)  # skip header
        edges = []
        for i, row in enumerate(reader):
            logging.info('Adding row numer: ' + str(i))
            edges.append(tuple(row))

        logging.info('Returning edges, size: ' + str(len(edges)))
        return edges

edges = load_edges()
g1=Graph.TupleList(edges, weights=True, directed=True)


# plot_graph(g1)
