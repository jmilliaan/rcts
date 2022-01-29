import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions

json_constants_file = open("constants.json")
json_constants = json.load(json_constants_file)

ig_url = json_constants["ig_url"]
rcts_username = json_constants["account_credentials"]["rcts_username"]
rcts_password = json_constants["account_credentials"]["rcts_password"]
number_of_posts = json_constants["number_of_posts"]
t_coef = json_constants["time_multiplier"]
chromedriver_location = json_constants["chromedriver_location"]


class RCTSChromeDriver:
    def __init__(self):
        self.username_box = None
        self.password_box = None
        self.search_box = None
        self.links = []

        chrome_options = Options()
        chrome_options.add_argument("--window-size=900,900")

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def open_instagram(self):
        self.driver.get(ig_url)
        time.sleep(t_coef * 2.5)

    def login(self, ig_username, ig_password):
        try:
            self.username_box = self.driver.find_element_by_css_selector("input[name='username']")
            self.password_box = self.driver.find_element_by_css_selector("input[name='password']")

            self.username_box.clear()
            self.password_box.clear()

            self.username_box.send_keys(ig_username)
            self.password_box.send_keys(ig_password)
            print("Login")
            self.driver.find_element_by_css_selector("button[type='submit']").click()
            print("Clicked Login Button")
            time.sleep(t_coef * 2.5)
        except selenium.common.exceptions.NoSuchElementException:
            print("> No Such Element Exception")
            pass

    def search_user(self, user):
        try:
            self.search_box = self.driver.find_element_by_css_selector("input[placeholder='Search']")
            time.sleep(t_coef * 0.5)
            self.search_box.clear()
            self.search_box.send_keys(user)
            time.sleep(t_coef * 1)
            self.search_box.send_keys(Keys.ENTER)
            time.sleep(t_coef * 1)
            self.search_box.send_keys(Keys.ENTER)
            time.sleep(t_coef * 2)
        except selenium.common.exceptions.NoSuchElementException:
            print("> No Such Element Exception")
            pass

    def scroll_down(self):
        try:
            self.driver.execute_script("window.scrollTo(0, "
                                       "document.body.scrollHeight);"
                                       "var lenOfPage=document.body.scrollHeight;"
                                       "return lenOfPage;")
            time.sleep(t_coef * 0.5)
        except selenium.common.exceptions.StaleElementReferenceException:
            print("> stale element reference exception")
            pass

    def get_links(self):
        try:
            self.links = self.driver.find_elements_by_tag_name('a')
            return self.links
        except selenium.common.exceptions.StaleElementReferenceException:
            print("> stale element reference exception")
            pass

    def close_driver(self):
        self.driver.close()
