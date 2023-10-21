import requests
import regex as re
import csv

#API_KEY = "AIzaSyA1wd2uv-yhQHYmKBh_cqG3g6cc7gCcp9k"
API_KEY = "AIzaSyCUiNyvyDnLaobCc25exIazE8bcBDZya7c"

TRENDS_URL = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&maxResults=[MAX_RES_NB]&regionCode=[REGION_CODE]&pageToken=[PAGE_TOKEN]&key=[YOUR_API_KEY]"

def load_stop_words():
    
    with open("stop_words_fr.csv", "r") as f:
        data = list(csv.reader(f, delimiter=","))
        data = [word[0].strip() for word in data]

    return data

def get_list(region_code, max_res):
    page_token = ""

    if max_res > 200:
        max_res = 200

    page_max = 50

    current_nb = 0

    titles = []
    desc = []
    tags = []

    while current_nb < max_res:

        if max_res < (page_max+current_nb):
            page_max = max_res - current_nb

        r = requests.get(TRENDS_URL.replace("[REGION_CODE]", region_code).replace("[YOUR_API_KEY]", API_KEY).replace("[MAX_RES_NB]", str(page_max)).replace("[PAGE_TOKEN]", page_token))
        
        rjson = r.json()
        
        titles.extend([vid["snippet"]["title"] for vid in rjson["items"]])
        desc.extend([vid["snippet"]["description"] for vid in rjson["items"]])
        tags.extend([" ".join(vid["snippet"]["tags"]) for vid in rjson["items"] if "tags" in vid["snippet"].keys()])

        current_nb += rjson["pageInfo"]["resultsPerPage"]
        try:
            page_token = rjson["nextPageToken"]
        except:
            page_token = ""
            break

    return (titles, desc, tags)

def get_words(strings):
    words = []
    
    for str in strings:
        str = str.replace(",", " ")
        str = re.sub(r'http\S+', '', str)
        str = re.sub(r'www\S+', '', str)
        str = re.sub(r'\S*@\S*\s?', '', str)
        words.extend(re.findall("[^\d_\W]+", str))

    words = [word.strip().lower() for word in words]

    return words

def count_words(words, stop_words):

    unique = list(dict.fromkeys(words))

    unique = [word for word in unique if (word.strip().encode() != b'\xef\xb8\x8f' and word not in stop_words)]

    counts = {}

    for word in unique:
        counts[word] = words.count(word)

    return counts

def print_res(count_dict, nb:int = None):
    res = sorted(count_dict.items(), key=lambda item: item[1], reverse=True)
    if nb != None:
    	res = res[:nb]
    for couple in res:
        print(couple)

def get_dict(loc, max):
    stop_words = load_stop_words()
    titles, desc, tags = get_list(loc, max)

    count_titles = count_words(get_words(titles), stop_words)

    count_desc = count_words(get_words(desc), stop_words)

    count_tags = count_words(get_words(tags), stop_words)

    return count_titles, count_desc, count_tags


def main():

    count_titles, count_desc, count_tags = get_dict("FR", 100)

    print("Titles")
    print_res(count_titles)
    print("\n========================\n")
    print("Descriptions")
    print_res(count_desc)
    print("\n========================\n")
    print("Tags")
    print_res(count_tags)

main()
