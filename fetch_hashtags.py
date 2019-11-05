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

def log(text):
    text = f'{text}\n'
    print(text)
    with open('data/log.txt', 'a+', encoding='utf-8') as log:
        log.write(text)


def save_hashtags(user_name):
    filename = f'data/tweets/{str(user_name)}'
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
    if not os.path.isdir('data'):
        os.mkdir('data')

    if not os.path.isdir('data/users'):
        log('Error: No "data/users" directory.')
        return

    log('\nInfo: New execution started.\n')

    counter = 0
    if not os.path.isdir('data/tweets'):
        os.mkdir('data/tweets')
        log('Info: Created "tweets" directory.')
    else:
        counter += len([filename for filename in os.listdir('data/tweets') if os.path.isfile(f'data/tweets/{filename}')])
        log(f'Info: Before execution tweets downloaded for {counter} users.')

    start_time = time.time()
    for filename in [user_file for user_file in os.listdir('data/users') if not os.path.isfile(f'data/tweets/{user_file}')]:
        if os.path.isfile(f'data/users/{filename}') and not os.path.isfile(f'data/tweets/{filename}'):
            counter += 1
            with open(f'data/users/{filename}', 'r', encoding='utf-8') as fr:
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
