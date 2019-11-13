import igraph
import datetime
import sys
import os


def find_communities_fastgreedy(g):
    communities = g.community_fastgreedy()
    clusters = communities.as_clustering()
    return clusters


def find_communities_edge_betweenness(g):
    # TODO nie wiem czy się zawiesza czy działa bardzo długo
    return
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
    g = igraph.read(graph_file_name)
    alg = sys.argv[2]
    if alg == 'fg':
        fg = find_communities_fastgreedy(g)
        # plot(g, fg)
    elif alg == 'eb':
        eb = find_communities_edge_betweenness(g)
        # plot(eb)
    elif alg == 'w':
        w = find_communities_walktrap(g)
        # plot(w)
    elif alg == 'ew':
        ew = find_communities_eigenvector(g)
        # plot(ew)
    elif alg == 's':
        pass
        # s = find_communities_spinglass(g)
        # plot(s)
    elif alg == 'lp':
        lp = find_communities_label_propagation(g)
        # plot(lp)
    elif alg == 'ml':
        ml = find_communities_multilevel(g)
        # plot(ml)
    elif alg == 'im':
        im = find_communities_infomap(g)
        # plot(im)
    elif alg == 'om':
        pass
        # om = find_communities_optimal_modularity(g)
        # plot(om)
    else:
        print('Incorrect second argument. Must be one of [fg, eb, w, ew, s, lp, ml, im, om]')
        return

    end_date = datetime.datetime.now()
    print(f'{sys.argv[1]},{alg},{(end_date - start_date).total_seconds()}')



if __name__ == '__main__':
    main()
