import re
import json
import datetime

json_constants_file = open("constants.json")
json_constants = json.load(json_constants_file)

comp_keywords = json_constants["competition_keywords"]
uni_keywords = json_constants["university_keywords"]

comp_pattern = "|".join(comp_keywords)
uni_pattern = "|".join(uni_keywords)

today = datetime.datetime.today()
this_year = today.year
this_month = today.month


def time_filtering(dataset):
    dataset["post year"] = dataset["Post Date"].str[:4].astype("int")
    dataset["post month"] = dataset["Post Date"].str[5:7].astype("int")

    last_year_index = dataset[dataset["post year"] < this_year].index
    last_month_index = dataset[dataset["post month"] < (this_month - 1 + 12) % 12].index

    dataset.drop(last_year_index, inplace=True)
    dataset.drop(last_month_index, inplace=True)
    return dataset


def duplicate_filter(dataset):
    lowercase = dataset["Caption"].str.lower()
    chars_only = []
    first_five = []

    for lowercase_caption in lowercase:
        char = re.findall(r"[\w']+|[.,!?;]", lowercase_caption)
        chars_only.append(char)
        first_five.append(f"{char[0]} {char[1]} {char[2]} {char[3]} {char[4]}")

    dataset["char only caption"] = chars_only
    dataset["first five"] = first_five

    dataset = dataset.drop_duplicates(subset="first five", keep="last")

    return dataset


def comp_univ_filter(dataset):
    is_competition = dataset["Caption"].str.contains(comp_pattern).astype(int)
    for_university = dataset["Caption"].str.contains(uni_pattern).astype(int)

    dataset["eligible"] = is_competition & for_university
    ineligible_index = dataset[dataset["eligible"] == 0].index

    dataset.drop(ineligible_index, inplace=True)
    dataset = dataset.drop(["post year", "post month", "char only caption", "first five", "eligible"], axis=1)

    dataset = dataset[["Date Acquired", "URL", "Username", "Post Date", "Caption", "Image URL"]]

    dataset.reset_index(drop=True, inplace=True)

    return dataset


def full_filter(dataset):
    time_filtered = time_filtering(dataset)
    duplicate_filtered = duplicate_filter(time_filtered)
    comp_uni_filtered = comp_univ_filter(duplicate_filtered)
    return comp_uni_filtered
