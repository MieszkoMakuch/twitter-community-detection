import igraph
import datetime
import sys
import os
import csv

DATA_DIR = '../data'


def save(g, clusters):
    print('Saving...')
    membership = clusters.membership
    writer = csv.writer(open(f"{DATA_DIR}/{sys.argv[1]}_{sys.argv[2]}.csv", "w"))
    writer.writerow(['Id', 'Label', 'Modularity Class'])
    for id, name, memb in zip(g.vs["id"], g.vs["label"], membership):
        writer.writerow([id, name, memb])


def find_communities_label_propagation(g):
    clusters = g.community_label_propagation()
    return clusters


def find_communities_multilevel(g):
    clusters = g.community_multilevel()
    return clusters


def find_communities_infomap(g):
    clusters = g.community_infomap()
    return clusters


def main():
    graph_file_name = f'{DATA_DIR}/graph_{sys.argv[1]}.gml'

    if not os.path.isfile(graph_file_name):
        print('First argument must be name of existing file with model')
        return

    start_date = datetime.datetime.now()
    print('Reading graph...')
    g = igraph.read(graph_file_name)
    alg = sys.argv[2]
    print('Looking for community')
    if alg == 'lp':
        lp = find_communities_label_propagation(g)
        save(g, lp)
    elif alg == 'ml':
        ml = find_communities_multilevel(g)
        save(g, ml)
    elif alg == 'im':
        im = find_communities_infomap(g)
        save(g, im)
    else:
        print('Incorrect second argument. Must be one of [lp, ml, im]')
        return

    end_date = datetime.datetime.now()
    print(f'{sys.argv[1]},{alg},{(end_date - start_date).total_seconds()}')


if __name__ == '__main__':
    main()
