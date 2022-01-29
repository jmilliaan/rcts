import json
import re

import selenium.common.exceptions

from rdataframe import RCTSDataframe
from google_api import SheetsAPI
from ig_post import InstagramPost
from rselenium import RCTSChromeDriver

json_constants_file = open("constants.json")
json_constants = json.load(json_constants_file)

ig_url = json_constants["ig_url"]
rcts_username = json_constants["account_credentials"]["rcts_username"]
rcts_password = json_constants["account_credentials"]["rcts_password"]
number_of_posts = json_constants["number_of_posts"]
t_coef = json_constants["time_multiplier"]

if __name__ == '__main__':
    rcts_api = SheetsAPI()
    dataset = RCTSDataframe()
    chrm = RCTSChromeDriver()

    chrm.open_instagram()
    chrm.login(rcts_username, rcts_password)
    c = 1

    for usr in rcts_api.accounts_df:
        print(c, usr)
        c += 1

        chrm.search_user(usr)
        chrm.scroll_down()
        links = chrm.get_links()
        post_count = 1

        for link in links:

            raw_url = link.get_attribute("href")
            url_contents = re.search("/p/", raw_url)
            if url_contents is not None:
                current_post = InstagramPost(raw_url)

                if current_post.success == 1:
                    dataset.add_all(new_url=current_post.url,
                                    username=current_post.username,
                                    post_date=current_post.post_date,
                                    caption=current_post.caption,
                                    image_url=current_post.image_url)
                    print(f"  {post_count} {current_post.url}")
                    post_count += 1

                if post_count == number_of_posts + 1:
                    break
            else:
                continue

    chrm.close_driver()

    dataset.filter_data()
    rcts_api.insert_rows(1, dataset.create_table())
