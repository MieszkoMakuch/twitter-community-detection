import networkx as nx
import os
import numpy as np
# import time
import datetime
# import igraph as ig
import sys

def time_print(text):
    print(f'{datetime.datetime.now()}: {text}')


def build_graph(graph_size):
    edges = []
    nodes = set()
    
    time_print('Builing graph...')
    
    for counter, filename in enumerate(os.listdir('data/users')[:graph_size]):
        username, file_extension = os.path.splitext(filename)
        if file_extension == '.json' and os.path.isfile(f'data/followers/{username}.csv'):
            with open(f'data/followers/{username}.csv', 'r', encoding='utf-8') as followers_file:
                followers = [line for line in followers_file.readlines()]
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
    graph_size = int(sys.argv[1])
    graphName = f'data/graph_{graph_size}.gml'
    if not os.path.isfile(graphName):
        G, nodes = build_graph(graph_size)
        time_print('Saving networkx graph...')
        nx.write_gml(G, graphName)


def save_community_detection_in_gephi_format(graph_community_fun, filename):
    time_print(f'Saving igraph to {filename}...')
    graph_community_fun().write_gml(filename)


if __name__ == '__main__':
    main()
