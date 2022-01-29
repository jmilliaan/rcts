import pandas as pd
from datetime import date
from filter import full_filter


class RCTSDataframe:
    def __init__(self):
        self.url = []
        self.username = []
        self.post_date = []
        self.caption = []
        self.image_url = []
        self.date_acquired = []
        self.dataframe = None
        self.filtered_data = None
        self.is_filtered = False
        self.table = None

    def add_url(self, new_url):
        self.url.append(new_url)

    def add_username(self, username):
        self.username.append(username)

    def add_post_date(self, post_date):
        self.post_date.append(post_date)

    def add_caption(self, caption):
        self.caption.append(caption)

    def add_image_url(self, image_url):
        self.image_url.append(image_url)

    def add_all(self, new_url, username, post_date, caption, image_url):
        self.url.append(new_url)
        self.username.append(username)
        self.post_date.append(post_date)
        self.caption.append(caption)
        self.image_url.append(image_url)

    def create_dataframe(self):
        today = date.today().strftime("%d/%m/%Y")
        for i in range(len(self.url)):
            self.date_acquired.append(today)
        dict_dataframe = {"URL": self.url,
                          "Username": self.username,
                          "Post Date": self.post_date,
                          "Caption": self.caption,
                          "Image URL": self.image_url,
                          "Date Acquired": self.date_acquired}

        self.dataframe = pd.DataFrame(dict_dataframe)
        return self.dataframe

    def filter_data(self):
        self.dataframe = self.create_dataframe()
        self.filtered_data = full_filter(self.dataframe)
        self.is_filtered = True
        return self.filtered_data

    def create_table(self):
        if not self.is_filtered:
            self.filter_data()
        self.table = self.filtered_data.values.tolist()
        return self.table

    def create_rows(self):
        today = date.today().strftime("%d/%m/%Y")
        for i in range(len(self.url)):
            self.date_acquired.append(today)
        big_row = []
        for i in range(len(self.url)):
            new_row = [self.date_acquired[i],
                       self.url[i],
                       self.username[i],
                       self.post_date[i],
                       self.caption[i],
                       self.image_url[i]]
            big_row.append(new_row)
        return big_row

    def df_to_csv(self, filename):
        self.dataframe.to_csv(filename)
