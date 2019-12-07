import csv
import sys
import os
import operator
import json
from pathlib import Path

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


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
            id = int(float(id))
            community = int(community)

            if community in communities:
                communities[community].append(user)
            else:
                communities[community] = [user]

        return communities


def get_community_hashtags(community_members):
    hashtags = {}
    for community_member in community_members:
        path = f'data/tweets/{community_member}.json'
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
    plt.savefig(f'data/wordmaps/{title}.png')


def main():
    if len(sys.argv) <= 1:
        print('First argument must be path to csv file with community vector of format[id, username, community_number].')
        return -1

    print('Parsing communities...')
    communities = parse_communities()
    print('Processing communities regarding hashtags...')
    communities_hashtags = [get_community_hashtags(community_members) for community, community_members in communities.items()]

    print('Sorting communities...')
    sorted_hashtag_communities = sorted(communities_hashtags, key=lambda hashtags: sum([count for hashtag, count in hashtags.items()]), reverse=True)
    top_hashtag_communities = sorted_hashtag_communities[:20]
    print('Creating strings from hashtags...')
    top_hashtag_communities_strings = [get_string_from_hashtags(community_hashtags) for community_hashtags in top_hashtag_communities]

    filename = Path(sys.argv[1]).stem
    for index, community_hashtags_string in enumerate(top_hashtag_communities_strings):
        if len(community_hashtags_string) > 0:
            print(f'Drawing community no {index + 1}...')
            show_wordcloud(community_hashtags_string, f'{filename}_{index + 1}')


if __name__ == '__main__':
    main()
