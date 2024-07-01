import pandas as pd
import requests
from typing import Dict
import requests
import json
import os

URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = os.environ['API']

# 1つ目の動画のコメント情報を取得
VIDEO_ID = 'pOfNvMKjdTk'


def print_video_comment(no, video_id, next_page_token, text_data):
    params = {
      'key': API_KEY,
      'part': 'snippet',
      'videoId': video_id,
      'order': 'relevance',
      'textFormat': 'plaintext',
      'maxResults': 100,
    }
    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()
    try :
        resource['items']
    except KeyError:
        return text_data.append('bad_id')

    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        # グッド数
        # like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
        # # 返信数
        reply_cnt = comment_info['snippet']['totalReplyCount']
        # # ユーザー名
        # user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
        # Id
        parentId = comment_info['snippet']['topLevelComment']['id']
        # # ユーザープロフィール情報
        # author_channel = comment_info["snippet"]['topLevelComment']['snippet']['authorChannelUrl']
        # リストに取得した情報を追加
        text_data.append([parentId, 'parent', text])
        # 処理確認用
        if len(text_data) % 100 == 0:
            print(len(text_data))
#     print('{:0=4}\t{}\t{}\t{}\t{}'.format(no, text.replace('\n', ' '), like_cnt, user_name, reply_cnt))
        if reply_cnt > 0:
            cno = 1
            print_video_reply(no, cno, video_id, next_page_token, parentId, text_data)
        no = no + 1

    if 'nextPageToken' in resource:
        print_video_comment(no, video_id, resource["nextPageToken"], text_data)
        

def print_video_reply(no, cno, video_id, next_page_token, id, text_data):
    params = {
      'key': API_KEY,
      'part': 'snippet',
      'videoId': video_id,
      'textFormat': 'plaintext',
      'maxResults': 50,
      'parentId': id,
      }

    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'comments', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['textDisplay']
        # # グッド数
        # like_cnt = comment_info['snippet']['likeCount']
        # # ユーザー名
        # user_name = comment_info['snippet']['authorDisplayName']
        # # ユーザープロフィール情報
        # author_channel = comment_info["snippet"]['authorChannelUrl']
        # リストに取得した情報を追加
        text_data.append([id, 'child', text])
#       print('{:0=4}-{:0=3}\t{}\t{}\t{}'.format(no, cno, text.replace('\n', ' '), like_cnt, user_name))
        cno = cno + 1

    if 'nextPageToken' in resource:
        print_video_reply(no, cno, video_id, resource["nextPageToken"], id, text_data)