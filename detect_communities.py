import igraph
import datetime
import sys
import os
import csv

def save(g, clusters):
    print('Saving...')
    membership = clusters.membership
    writer = csv.writer(open(f"data/{sys.argv[1]}_{sys.argv[2]}.csv", "w"))
    writer.writerow(['Id', 'Label', 'Modularity Class'])
    for id, name, memb in zip(g.vs["id"], g.vs["label"], membership):
        writer.writerow([id, name, memb])


def find_communities_fastgreedy(g):
    communities = g.community_fastgreedy()
    clusters = communities.as_clustering()
    return clusters


def find_communities_edge_betweenness(g):
    # TODO nie wiem czy sie zawiesza czy dziala bardzo dlugo
    communities = g.community_edge_betweenness()
    clusters = communities.as_clustering()
    return clusters


def find_communities_walktrap(g):
    communities = g.community_walktrap()
    clusters = communities.as_clustering()
    return clusters


def find_communities_eigenvector(g):
    clusters = g.community_leading_eigenvector()
    return clusters


def find_communities_spinglass(g):
    # TODO split into connected parts
    return


def find_communities_label_propagation(g):
    clusters = g.community_label_propagation()
    return clusters


def find_communities_multilevel(g):
    clusters = g.community_multilevel()
    return clusters


def find_communities_infomap(g):
    clusters = g.community_infomap()
    return clusters


def find_communities_optimal_modularity(g):
    # TODO GLPK not implemented ???
    return
    communities = g.community_optimal_modularity()
    clusters = communities.as_clustering()
    return clusters


def main():
    graph_file_name = f'data/graph_{sys.argv[1]}.gml'

    if not os.path.isfile(graph_file_name):
        print('First argument must be name of existing file with model')
        return

    start_date = datetime.datetime.now()
    print('Reading graph...')
    g = igraph.read(graph_file_name)
    alg = sys.argv[2]
    print('Looking for community')
    if alg == 'fg':
        pass
        # fg = find_communities_fastgreedy(g)
        # save(g, fg)
    elif alg == 'eb':
        pass
        # eb = find_communities_edge_betweenness(g)
        # save(eb)
    elif alg == 'w':
        pass
        # w = find_communities_walktrap(g)
        # save(w)
    elif alg == 'ew':
        pass
        # ew = find_communities_eigenvector(g)
        # save(g, ew)
    elif alg == 's':
        pass
        # s = find_communities_spinglass(g)
        # save(g, s)
    elif alg == 'lp':
        lp = find_communities_label_propagation(g)
        save(g, lp)
    elif alg == 'ml':
        ml = find_communities_multilevel(g)
        save(g, ml)
    elif alg == 'im':
        im = find_communities_infomap(g)
        save(g, im)
    elif alg == 'om':
        pass
        # om = find_communities_optimal_modularity(g)
        # save(om)
    else:
        print('Incorrect second argument. Must be one of [fg, eb, w, ew, s, lp, ml, im, om]')
        return

    end_date = datetime.datetime.now()
    print(f'{sys.argv[1]},{alg},{(end_date - start_date).total_seconds()}')


if __name__ == '__main__':
    main()
