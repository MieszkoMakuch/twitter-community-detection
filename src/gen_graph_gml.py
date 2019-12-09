import networkx as nx
import os
import numpy as np
# import time
import datetime
# import igraph as ig
import sys

DATA_DIR = '../data'
USERS_DIR = f'{DATA_DIR}/users'
FOLLOWERS_DIR = f'{DATA_DIR}/followers'


def time_print(text):
    print(f'{datetime.datetime.now()}: {text}')


def build_graph():
    edges = []
    nodes = set()

    time_print('Builing graph...')

    for counter, filename in enumerate(os.listdir(USERS_DIR)):
        username, file_extension = os.path.splitext(filename)
        if file_extension == '.json' and os.path.isfile(f'{FOLLOWERS_DIR}/{username}.csv'):
            with open(f'{FOLLOWERS_DIR}/{username}.csv', 'r', encoding='utf-8') as followers_file:
                followers = [follower for follower in followers_file.read().splitlines() if os.path.isfile(f'{USERS_DIR}/{follower}.json')]
                edges += [(follower, username) for follower in followers]
                nodes.update(followers + [username])

        if counter % 1000 == 0:
            time_print(f'{counter} files opened')


    time_print('Processing edges...')
    edges = list(set(tuple(sorted(edge)) for edge in edges))
    time_print('Processing nodes...')
    nodes = list(set(nodes))
    G = nx.Graph()
    time_print('Adding nodes to graph...')
    G.add_nodes_from(nodes)
    time_print('Adding edges to graph...')
    G.add_edges_from(edges)

    return G, nodes


def main():
    name = sys.argv[1]
    graph_name = f'{DATA_DIR}/graph_{name}.gml'
    if not os.path.isfile(graph_name):
        G, nodes = build_graph()
        time_print('Saving networkx graph...')
        nx.write_gml(G, graph_name)


if __name__ == '__main__':
    main()
