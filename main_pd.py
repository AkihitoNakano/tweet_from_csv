import pandas as pd
import tweepy
import head_key as ky
import random
from datetime import datetime
from typing import List

class TweetProveb:
    def __init__(self, client, csv_file):
        self.csv = csv_file
        self.tweet_content=''
        # CSVを開いてツイート文を作成
        self.open_csv()
        # 回数と更新日を更新して書き出し
        self.update_list()


    def open_csv(self):
        self.df = pd.read_csv(self.csv)
        self.index = random.randint(0,len(self.df)-1)
        pick_row = self.df.iloc[self.index, :]
        self.tweet_content = f'{pick_row.loc["コンテンツ"]}  -{pick_row.loc["名前"]}'

        # ツイート
        client.create_tweet(text=self.tweet_content)

    def update_list(self):
        self.df.loc[self.index,'回数'] += 1
        today = datetime.now().strftime('%Y/%m/%d')
        self.df.loc[self.index,'更新日'] = today
        print(self.df.loc[self.index,:])

        # 書き出し
        self.df.to_csv(self.csv, index=False)






if __name__ == "__main__":
    client = tweepy.Client(ky.bearer_token, ky.api_key, ky.api_secret,
                           ky.access_token, ky.access_secret)

    csv_file = 'list.csv'

    TweetProveb(client, csv_file)
