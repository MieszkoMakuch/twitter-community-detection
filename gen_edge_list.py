import glob
import json
import os

FOLLOWING_DIR = 'test-followers'
USERS_DIR = 'test-users'


# FOLLOWING_DIR = '../Dane/following-korwin4'
# USERS_DIR = '../Dane/twitter-users-korwin4'

# FOLLOWING_DIR = 'following-korwin-test-data'
# USERS_DIR = 'twitter-users-korwin-test-data'


def process_user(edges_csv, followers_file, username):
    followers = [line.strip() for line in open(followers_file, encoding="utf-8")]
    weight = get_followers_count(username)  # TODO maybe it would be better to use following count of the follower?

    for follower in followers:
        if os.path.exists(get_user_filepath(follower)):
            edge = (follower, username, weight)
            edges_csv.write('%s,%s,%d\n' % (edge[0], edge[1], edge[2]))


def get_user_filepath(username_):
    return os.path.join(USERS_DIR, username_ + '.json')


def filepath_to_username(file):
    base = os.path.basename(file)
    return os.path.splitext(base)[0]


def get_followers_count(username):
    with open(get_user_filepath(username), 'r', encoding='utf-8') as user_file:
        data = json.load(user_file)
        return data['followers']


# Generates csv containing edges with weights based on files in FOLLOWING_DIR (csv) and USERS_DIR (json)
with open('twitter_network.csv', 'w') as edges_csv:
    edges_csv.write('Source,Target,weight\n')

    for i, followers_file in enumerate(glob.glob('%s/*.csv' % FOLLOWING_DIR)):
        username = filepath_to_username(followers_file)
        if os.path.exists(get_user_filepath(username)):
            print('Processing file ' + followers_file + ' index: ' + str(i))
            process_user(edges_csv, followers_file, username)
        else:
            print('No user file for user: ' + username)
