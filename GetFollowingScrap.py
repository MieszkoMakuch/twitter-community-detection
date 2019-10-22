from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

import json
import logging
import os
import time

import tweepy
import twint

# logger configuration
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

FOLLOWING_DIR = 'following-new'
USER_DIR = 'twitter-users-new'
MAX_FRIENDS = 200
FRIENDS_OF_FRIENDS_LIMIT = 200

# Create the directories we need
if not os.path.exists(FOLLOWING_DIR):
    os.makedirs(FOLLOWING_DIR)

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)


def get_user(username):
    c = twint.Config()
    c.Username = username
    c.Custom["users"] = ["id", "username"]  # TODO - try to remove it
    c.Output = os.path.join(USER_DIR, username + '.json')
    c.Store_json = True
    c.Hide_output = True
    twint.run.Lookup(c)


def get_followers(username):
    c = twint.Config()
    c.Username = username
    c.Store_object = True
    c.Limit = 200
    c.Hide_output = True
    twint.run.Followers(c)
    return twint.output.follows_list


def get_follower_ids(username, max_depth=2, current_depth=0, taboo_list=[]):
    if current_depth == max_depth:  # TODO - probably should be removed
        logging.info('out of depth')
        return taboo_list

    if username in taboo_list:
        # we've been here before
        logging.info('Already been here.')
        return taboo_list
    else:
        taboo_list.append(username)

    followers_fname = os.path.join(FOLLOWING_DIR, username + '.csv')
    try:
        user_fname = os.path.join(USER_DIR, str(username) + '.json')
        if not os.path.exists(user_fname):
            logging.info('Retrieving user details for twitter id %s' % str(username))
            while True:
                try:
                    get_user(username)
                    break
                except Exception as error:
                    logging.exception('Error while getting user inforation ' + username)
                    return taboo_list

        user = json.loads(open(user_fname, encoding="utf-8").read())
        username = user['username']
        followers_fname = os.path.join(FOLLOWING_DIR, username + '.csv')
        friendids = []

        if not os.path.exists(followers_fname):
            logging.info('No cached data for screen name "%s"' % username)
            with open(followers_fname, 'w', encoding="utf-8") as followers_file:
                params = (user['username'], username)
                logging.info('Retrieving friends for user "%s" (%s)' % params)

                followers = get_followers(user['username'])
                friend_count = 0
                for friend_name in followers:
                    try:
                        friendids.append(friend_name)
                        followers_file.write('%s\n' % friend_name)
                        friend_count += 1
                        if friend_count >= MAX_FRIENDS:
                            logging.info('Reached max no. of friends for "%s".' % friend_name)
                            break
                    except tweepy.TweepError:
                        # hit rate limit, sleep for 15 minutes
                        logging.info('Rate limited. Sleeping for 15 minutes.')
                        time.sleep(15 * 60 + 15)
                        continue
                    except StopIteration:
                        break

        else:
            friendids = [line.strip().split('\t')[0] for line in open(followers_fname, encoding="utf-8")]

        logging.info('Found %d friends for %s' % (len(friendids), username))

        # get friends of friends
        cd = current_depth
        if cd + 1 < max_depth:
            for fid in friendids[:FRIENDS_OF_FRIENDS_LIMIT]:
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                                              current_depth=cd + 1, taboo_list=taboo_list)

        if cd + 1 < max_depth and len(friendids) > FRIENDS_OF_FRIENDS_LIMIT:
            logging.info('Not all friends retrieved for %s.' % username)

    except Exception as error:
        logging.exception('Error retrieving followers for user username: ' + username, exc_info=True)

        if os.path.exists(followers_fname):
            os.remove(followers_fname)
            logging.warn('Removed file "%s".' % followers_fname)
        time.sleep(2)
    return taboo_list


if __name__ == '__main__':
    depth = 20
    logging.info('Max Depth: %d' % depth)

    c = twint.Config()
    c.Username = "a_humane_being"
    c.Store_object = True
    twint.run.Lookup(c)
    user_start = twint.output.users_list
    logging.info(get_follower_ids(user_start[0].username, max_depth=depth))
