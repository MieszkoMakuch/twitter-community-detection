import glob
import os
import json
import sys
import argparse
import csv
from collections import defaultdict


SEED = 'JkmMikke'


USERS_DIR = 'test-users'
FOLLOWING_DIR = 'test-followers'

users = defaultdict(lambda: { 'followers': 0 })

for f in glob.glob('%s/*.json' % USERS_DIR):
    print("loading " + str(f))
    data = json.load(open(f, encoding="utf-8"))
    username = data['username']
    users[username] = {'followers': data['followers'], 'id':data['id']}

def process_follower_list(screen_name, edges=[], depth=0, max_depth=5):
    f = os.path.join('%s' % FOLLOWING_DIR, screen_name + '.csv')
    print("processing " + str(f))

    if not os.path.exists(f):
        return edges

    # followers = [line.strip().split(',') for line in file(f)] # TODO - debug
    followers = [line.strip() for line in open(f, encoding="utf-8")]

    # csv_rows = list(csv.reader(open(f, encoding="utf-8")))
    # if len(csv_rows) == 0:
    #     print("empty friend ids: " + f)
    #     followers = []
    # else:
    #     followers = csv_rows[0]

    print('Followers:')
    print(*followers)

    for follower_username in followers:
        print('Follower data: ' + follower_username)
        if len(follower_username) == 0:
            continue

        # use the number of followers for screen_name as the weight
        weight = users[screen_name]['followers']
        print('weight: ' + str(weight))

        edges.append([screen_name, follower_username, weight])

        if depth+1 < max_depth:
            process_follower_list(follower_username, edges, depth+1, max_depth)

    return edges

edges = process_follower_list(SEED, max_depth=5)

with open('twitter_network.csv', 'w') as outf:
    edge_exists = {}
    outf.write('user,follower,weight\n')
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not(key in edge_exists):
            outf.write('%s,%s,%d\n' % (edge[0], edge[1], edge[2]))
            edge_exists[key] = True
