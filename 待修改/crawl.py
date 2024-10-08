# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import wordcloud
import requests
import logging
import jieba
import json

jieba.setLogLevel(logging.INFO)


def get_resp() -> requests.Response:
    """
    send a request
    :return: response
    """

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    url = "https://weibo.com/ajax/side/hotSearch"

    response = requests.get(url=url, headers=headers)

    status_code = response.status_code
    if status_code != 200:
        print("An error with response.")

    get_data(response)


def get_data(response):
    """
    get the ming(top search and hot search)
    :return: None
    """

    with open(file="search.txt", mode="a", encoding="utf-8") as f:

        search_json = json.loads(response.text)
        search_top: str = search_json["data"]["realtime"][0]["note"]
        f.write(search_top + "\n")
        print(f"top search: {search_top}")

        for num in range(0, 50):
            search: str = search_json["data"]["realtime"][num]["note"]
            f.write(search + "\n")
            print(f"hot search: {search}")

    return None


def search_wordcloud():
    """
    plot the wordcloud
    :return: None
    """

    # use the stopwords
    with open("stopwords.txt", mode="r", encoding="utf-8") as stop_file:
        stopwords: list = stop_file.readlines()
    stopwords = [word.strip() for word in stopwords]

    # words you need to delete
    word_delete: list = []
    stopwords.extend(word_delete)

    with open("search.txt", "r", encoding="utf-8") as search_file:
        search_file_read = search_file.read()

    ls = jieba.lcut(search_file_read)
    ls = [word for word in ls if word not in stopwords]
    txt = " ".join(ls)

    word_cloud = wordcloud.WordCloud(
        font_path="msyh.ttc",
        width=1000,
        height=700,
        background_color="white",
                           )
    word_cloud.generate(txt)

    word_cloud.to_file("search.png")

    return None


def main():

    try:
        # get the ming and write to a txt 文件读写
        get_resp()

        # wordcloud
        search_wordcloud()

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")


if __name__ == '__main__':
    main()






