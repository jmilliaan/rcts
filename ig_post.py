import requests
import html
import json
from datetime import datetime
import requests

# session = requests.Session()
# session.get("https://www.instagram.com")
# cookies = session.cookies.get_dict()
json_constants_file = open("constants.json")
json_constants = json.load(json_constants_file)


def get_cookies(input_url):
    session = requests.Session()
    session.get(input_url)
    cookies = session.cookies.get_dict()
    return str(cookies)


class InstagramPost:
    def __init__(self, url, header=""):
        self.url = url
        # self.header = header
        self.header = json_constants["header"]
        self.username = ""
        self.post_date = ""
        self.caption = ""
        self.image_url = ""
        self.extension = "?__a=1"
        self.json_url = self.url + self.extension

        # self.header["cookie"] = str(self.json_text.cookies.get_dict())
        self.json_text = requests.get(self.json_url, headers=self.header)

        self.html_text = html.unescape(self.json_text.text)
        self.head = self.html_text[:9]
        self.json_data = []

        self.success = 0

        if self.head == '{"items":':
            try:
                self.json_data = json.loads(self.html_text)
                items = self.json_data["items"][0]
                if items["media_type"] == 8:
                    self.image_url = items['carousel_media'][0]["image_versions2"]["candidates"][0]["url"]

                elif items["media_type"] == 1:
                    self.image_url = items["image_versions2"]["candidates"][0]["url"]

                self.username = items["user"]["username"]
                unix_time = int(items["taken_at"])
                self.post_date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')
                self.caption = items["caption"]["text"]
                self.success = 1
            except json.decoder.JSONDecodeError:
                print("json.decoder.JSONDecodeError")
                pass
            except IndexError or TypeError:
                print("IndexError or TypeError ")
                self.post_date = ""
                self.caption = ""
                self.image_url = ""
                pass
        # OLD INSTAGRAM API:
        # if self.head == '{"graphql':
        #     try:
        #         self.json_data = json.loads(self.html_text)
        #         body = self.json_data["graphql"]["shortcode_media"]
        #         edges = body["edge_media_to_caption"]["edges"]
        #         self.username = body["owner"]["username"]
        #         self.post_date = detect_date(str(self.json_data))
        #         self.caption = edges[0]["node"]["text"].strip()
        #         self.image_url = body["display_url"]
        #         self.success = 1
