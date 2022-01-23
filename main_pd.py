import pandas as pd
import tweepy
import head_key as ky
import random
from datetime import datetime


class TweetProveb:
    def __init__(self, client, csv_file):
        self.csv = csv_file
        self.tweet_content = ''
        # CSVを開いてツイート文を作成&ツイート
        self.open_csv()
        # 回数と更新日を更新して書き出し
        self.update_list()

    def open_csv(self):
        self.df = pd.read_csv(self.csv)
        # 回数が最も少ないグループを作る
        min_val = self.df['回数'].min()
        new_df = self.df[self.df['回数']==min_val]
        # 重みを考慮した列を回数が最も少ないグループ
        df_02 = self.df[(self.df['回数']> min_val) & (self.df['重み'] >1)]
        df_02 = df_02.assign(value = df_02['重み']-df_02['回数'])
        df_02 = df_02[df_02['value']>=min_val]

        # 回数最小グループと重みを考慮したグループをマージする
        new_df = pd.concat([new_df,df_02])

        # インデックス番号を振り直す
        new_df.reset_index(inplace=True)
        print(new_df)

        temp_ids = random.randint(0, len(new_df)-1)
        pick_row = new_df.iloc[temp_ids, :]
        self.index = pick_row['index']
        self.tweet_content = f'{pick_row.loc["コンテンツ"]}  -{pick_row.loc["名前"]}'
        print(self.tweet_content)
        # ツイート
        client.create_tweet(text=self.tweet_content)

    def update_list(self):
        self.df.loc[self.index, '回数'] += 1
        today = datetime.now().strftime('%Y/%m/%d')
        self.df.loc[self.index, '更新日'] = today

        # 書き出し
        self.df.to_csv(self.csv, index=False)


if __name__ == "__main__":
    client = tweepy.Client(ky.bearer_token, ky.api_key, ky.api_secret,
                           ky.access_token, ky.access_secret)

    csv_file = 'list.csv'

    TweetProveb(client, csv_file)
