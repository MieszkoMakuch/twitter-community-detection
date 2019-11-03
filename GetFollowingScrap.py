from __future__ import print_function
from __future__ import print_function
from __future__ import print_function

import csv
import json
import logging
import os
import shutil
import time

import twint
from pathlib import Path

# logger configuration
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

FOLLOWING_DIR = 'following-korwin-test-data'
USER_DIR = 'twitter-users-korwin-test-data'
MAX_FRIENDS = 200
FRIENDS_OF_FRIENDS_LIMIT = 200

# Create the directories we need
if not os.path.exists(FOLLOWING_DIR):
    os.makedirs(FOLLOWING_DIR)

if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)


def get_user(username, path):
    c = twint.Config()
    c.Username = username
    c.Custom["users"] = ["id", "username"]  # TODO - try to remove it
    c.Output = path + '-tmp.json'
    c.Store_json = True
    c.Hide_output = True
    twint.run.Lookup(c)
    # twint saves file as path-tpm.json, then the file is moved to path.json to prevent multiple threads from
    # writing to the same file
    shutil.move(path + '-tmp.json', path + '.json')


def save_followers(username, path):
    tmp_path = path + '-tmp.csv'
    final_path = path + '.csv'
    Path(tmp_path).touch()
    logging.info('Getting followers for: ' + username)
    try:
        c = twint.Config()
        c.Username = username
        c.Output = tmp_path
        c.Store_csv = True
        c.Limit = MAX_FRIENDS
        c.Hide_output = True
        twint.run.Followers(c)
        shutil.move(tmp_path, final_path)
    except Exception as error:
        logging.exception('Error while saving followers for user ' + username, exc_info=True)
        if os.path.exists(final_path):
            os.remove(final_path)


def get_follower_ids(username, max_depth=2, current_depth=0, taboo_list=[]):
    logging.info('Current depth: ' + str(current_depth) + ' username=' + username)
    if current_depth == max_depth:  # TODO - probably should be removed
        logging.info('out of depth')
        return taboo_list

    if username in taboo_list:
        # we've been here before
        logging.info('Already been here: ' + username)
        return taboo_list
    else:
        taboo_list.append(username)

    followers_fname= os.path.join(FOLLOWING_DIR, username)
    followers_fname_extension = followers_fname + '.csv'
    followers_fname_tmp = followers_fname + '-tmp.csv'
    logging.debug('followers fname: ' + followers_fname_extension)
    try:
        user_fname = os.path.join(USER_DIR, str(username))
        user_fname_extension = user_fname + '.json'
        if not os.path.exists(user_fname_extension):
            logging.info('Retrieving user details for twitter id %s' % str(username))
            try:
                get_user(username, user_fname)
            except Exception as error:
                logging.exception('Error while getting user inforation ' + username)
                return taboo_list
        user = json.loads(open(user_fname_extension, encoding="utf-8").read())
        username = user['username']
        # follower_ids = []

        if os.path.exists(followers_fname_tmp):
            logging.info('Skipping - some other process is now downloading followers for this user: ' + username)
            return taboo_list

        if not os.path.exists(followers_fname_extension):
            logging.info('No cached data for screen name "%s", saving followers' % username)
            save_followers(username, followers_fname)

        follower_ids = [line.strip() for line in open(followers_fname_extension, encoding="utf-8")]
        # follower_ids = follower_ids[1:] # ignore first line - it is always a 'username'

        # get friends of friends
        cd = current_depth
        if cd + 1 < max_depth:
            for fid in follower_ids[:FRIENDS_OF_FRIENDS_LIMIT]:
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                                              current_depth=cd + 1, taboo_list=taboo_list)
        else:
            logging.info('Followers of ' + username + ' will not be analyzed - reached max depth current=' + str(current_depth))

        if cd + 1 < max_depth and len(follower_ids) > FRIENDS_OF_FRIENDS_LIMIT:
            logging.info('Not all friends retrieved for %s.' % username)
    except ValueError as error:
        logging.exception('Error retrieving followers for user username: ' + username, exc_info=True)
    except Exception as error:
        logging.exception('Error retrieving followers for user username: ' + username, exc_info=True)

        if os.path.exists(followers_fname_extension):
            os.remove(followers_fname_extension)
            logging.warning('Removed file "%s".' % followers_fname_extension)

        tts = 60
        logging.info('Sleeping for ' + str(tts) + ' seconds')
        time.sleep(tts)
    return taboo_list

def clean_tmp():
    import os
    import glob
    fileList = glob.glob(FOLLOWING_DIR + '/*tmp.csv')
    print('Cleaning tmp files; ')
    print(*fileList)
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)



if __name__ == '__main__':
    try:
        depth = 6
        logging.info('Max Depth: %d' % depth)

        c = twint.Config()
        c.Username = "JkmMikke"
        c.Store_object = True
        twint.run.Lookup(c)
        user_start = twint.output.users_list
        logging.info(get_follower_ids(user_start[0].username, max_depth=depth))
    except (KeyboardInterrupt, SystemExit): # http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.html
        clean_tmp()
        raise
