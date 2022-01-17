import tweepy
import head_key as ky
import csv
import random
from datetime import datetime


class TweetProverb:
    def __init__(self, client, csv_file):
        self.csv_file = csv_file
        self.tweet_content = ''
        # headerを取得
        self.header = self.get_header()
        # CSVを読み込んでツイート
        self.info = self.open_csv()
        # カウント数や更新日をアップデート
        new_list = self.update_list(self.info)
        # CSVに新しいリストを書き込む
        self.write_csv(new_list)

    def get_header(self):
        with open(self.csv_file, encoding='sjis',newline='') as f:
            reader = csv.reader(f)
            list = [i for i in reader]
            header = list[0]
            return header


    def open_csv(self):
        with open(self.csv_file, encoding='sjis') as f:
            reader = csv.reader(f)
            head = next(reader)
            data = [row for row in reader]
            show_num = random.randint(0, len(data) - 1)
            content, name, tag, weight, count, date = data[show_num]
            today = datetime.today()
            today = today.strftime('%Y/%m/%d')
            date = today
            self.tweet_content = f'{content} -{name}'
            return data, show_num, count , date


    def update_list(self, info):
        data, show_num, count, day = info
        data[show_num][4] = int(count) + 1
        data[show_num][5] = day
        data.insert(0, self.header)
        return data

    def write_csv(self, new_list):
        with open(self.csv_file, 'w',) as f:
            writer = csv.writer(f)
            for row in new_list:
                writer.writerow(row)


# client.create_tweet(text=content.text)

if __name__ == "__main__":
    client = tweepy.Client(ky.bearer_token, ky.api_key, ky.api_secret,
                           ky.access_token, ky.access_secret)

    csv_file = 'tips.csv'

    TweetProverb(client, csv_file)
