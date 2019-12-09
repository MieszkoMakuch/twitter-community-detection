import csv
import sys
import os
import operator
import json
from pathlib import Path

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

DATA_DIR = '../data'
TWEETS_DIR = f'{DATA_DIR}/tweets'
WORDMAPS_DIR = f'{DATA_DIR}/wordmaps'


def parse_communities():
    with open(sys.argv[1], encoding="utf-8") as community_file:
        csv_reader = csv.reader(community_file, delimiter=',')
        communities = {}
        next(community_file, None)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if len(row) == 0:
                continue

            [id, user, community] = row
            community = int(community)

            if community in communities:
                communities[community].append(user)
            else:
                communities[community] = [user]

        return communities


def get_community_hashtags(community_members):
    hashtags = {}
    for community_member in community_members:
        path = f'{TWEETS_DIR}/{community_member}.json'
        if not os.path.isfile(path):
            continue
        with open(path, 'r', encoding="utf-8") as hashtags_file:
            try:
                member_hashtags = json.load(hashtags_file)
                for hashtag, count in member_hashtags.items():
                    if hashtag in hashtags:
                        hashtags[hashtag] += count
                    else:
                        hashtags[hashtag] = count
            except:
                continue

    return hashtags


def get_string_from_hashtags(hashtags):
    res = ''
    for hashtag, count in hashtags.items():
        res += ((' ' + hashtag) * count)

    return res


def show_wordcloud(text, title = None):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1,
        collocations=False
    ).generate(text)

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')

    plt.imshow(wordcloud)
    plt.savefig(f'{WORDMAPS_DIR}/{title}.png')


def main():
    if len(sys.argv) <= 1:
        print('First argument must be path to csv file with community vector of format[id, username, community_number].')
        return -1

    print('Parsing communities...')
    communities = parse_communities()
    sorted_communities = sorted(communities.values(), key=lambda v: len(v), reverse=True)

    largest_communities = sorted_communities[:min(len(sorted_communities) // 3, 10)]
    medium_communities = sorted_communities[
                                 len(sorted_communities) // 2 - min(len(sorted_communities) // 6, 5):len(sorted_communities) // 2 + min(len(sorted_communities) // 6, 5)]
    smallest_communities = sorted_communities[-min(len(sorted_communities) // 3, 10):]
    picked_communities = smallest_communities + medium_communities + largest_communities

    print('Processing communities regarding hashtags...')
    communities_hashtags = [get_community_hashtags(community_members) for community_members in picked_communities]
    communities_hashtags_strings = [get_string_from_hashtags(community_hashtags) for community_hashtags in communities_hashtags]

    filename = Path(sys.argv[1]).stem
    for index, community_hashtags_string in enumerate(communities_hashtags_strings):
        if len(community_hashtags_string) > 0:
            print(f'Drawing community no {index + 1}...')
            show_wordcloud(community_hashtags_string, f'{filename}_{index + 1}')


if __name__ == '__main__':
    main()
