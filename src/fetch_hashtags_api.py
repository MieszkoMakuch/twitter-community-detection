import json
import os
import csv
import tweepy
import time

env_file = open(f'.env.json', 'r')
env = json.load(env_file)
env_file.close()

auth = tweepy.OAuthHandler(env['consumer_key'], env['consumer_secret'])
auth.set_access_token(env['access_token'], env['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

DATA_DIR = '../data'
HASHTAGS_DIR = f'{DATA_DIR}/tweets'
USERS_DIR = f'{DATA_DIR}/users'


def log(text):
    text = f'{text}\n'
    print(text)
    with open(f'{DATA_DIR}/fetch_hashtags_log.txt', 'a+', encoding='utf-8') as log:
        log.write(text)


def save_hashtags(user_name):
    filename = f'{HASHTAGS_DIR}/{str(user_name)}'
    if not os.path.isfile(filename):
        user_hashtags = {}
        try:
            for page in tweepy.Cursor(api.user_timeline, screen_name=user_name, count=200).pages(5):
                for tweet in page:
                    hashtags = [hashtag_entity['text'] for hashtag_entity in tweet.entities['hashtags']]
                    for hashtag in hashtags:
                        if hashtag in user_hashtags:
                            user_hashtags[hashtag] += 1
                        else:
                            user_hashtags[hashtag] = 1
        except:
            log(f'Error: Unauthorized {user_name}')

        with open(f'{filename}.json', 'w+', encoding='utf-8') as fw:
            json.dump(user_hashtags, fw)


def fetch_hashtags():
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    if not os.path.isdir(USERS_DIR):
        log(f'Error: No "{USERS_DIR}" directory.')
        return

    log('\nInfo: New execution started.\n')

    counter = 0
    if not os.path.isdir(HASHTAGS_DIR):
        os.mkdir(HASHTAGS_DIR)
        log(f'Info: Created "{HASHTAGS_DIR}" directory.')
    else:
        counter += len([filename for filename in os.listdir(HASHTAGS_DIR) if os.path.isfile(f'{HASHTAGS_DIR}/{filename}')])
        log(f'Info: Before execution tweets downloaded for {counter} users.')

    start_time = time.time()
    for filename in [user_file for user_file in os.listdir(USERS_DIR) if not os.path.isfile(f'{HASHTAGS_DIR}/{user_file}')]:
        if os.path.isfile(f'{USERS_DIR}/{filename}') and not os.path.isfile(f'{HASHTAGS_DIR}/{filename}'):
            counter += 1
            with open(f'{USERS_DIR}/{filename}', 'r', encoding='utf-8') as fr:
                try:
                    data = json.load(fr)
                    username = data['username']
                    save_hashtags(username)
                    log(f'{counter}. {time.time() - start_time} {username}')
                    start_time = time.time()
                except:
                    log(f'Error: JSON {filename}')


    log(f'Info: After execution tweets downloaded for {counter} users.')

if __name__ == "__main__":
    fetch_hashtags()
