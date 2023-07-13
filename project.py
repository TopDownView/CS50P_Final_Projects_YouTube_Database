from googleapiclient.discovery import build
import json
import re
from tabulate import tabulate
from tqdm import tqdm


def main() -> None:
    """
    Per Youtube Data API docs
    """
    API_KEY = # Private API Key goes here as a str
    YOUTUBE = build("youtube", "v3", developerKey=API_KEY)
    """
    Welcome message
    """
    print("-------------------------------------------------")
    print("Welcome to CS50P Final Projects YouTube Database!")
    print("-------------------------------------------------")
    """
    Execution of functions

    Every list returned by a function is saved as a JSON file.

    Functions from 'get_search_results(YOUTUBE)' to 'write_json_file(final_data_, "final_data.json")'
    can be commented out after the program is executed if the user doesn't want to make additional
    API queries and instead wants to play around and sort the data using 'final_data.json' file.

    P.S. One execution of the program 'costs' cca 1600 API queries: the daily quota is 10k,
    per Youtube Data API docs.
    """
    get_search_results_ = get_search_results(YOUTUBE)  # Comment out from here...
    write_json_file(get_search_results_, "search_results.json")
    read_json_file_1 = read_json_file("search_results.json")
    selected_search_results_ = selected_search_results(read_json_file_1)
    write_json_file(selected_search_results_, "selected_search_results.json")
    read_json_file_2 = read_json_file("selected_search_results.json")
    regex_check_ = regex_check(read_json_file_2)
    write_json_file(regex_check_, "regex_check.json")
    read_json_file_3 = read_json_file("regex_check.json")
    get_video_ids_ = get_video_ids(read_json_file_3)
    write_json_file(get_video_ids_, "video_ids.json")
    read_json_file_4 = read_json_file("video_ids.json")
    get_video_stats_ = get_video_stats(YOUTUBE, read_json_file_4)
    write_json_file(get_video_stats_, "video_stats.json")
    read_json_file_5 = read_json_file("video_stats.json")
    final_data_ = final_data(read_json_file_5)
    write_json_file(final_data_, "final_data.json")  # ...to here
    read_json_file_6 = read_json_file("final_data.json")
    """
    While loop keeps the program opened until Ctrl + D is pressed:
    this way, there are no new API calls if the user wants to sort the data in a different way.
    """
    while True:
        try:
            sort, sort_order = user_input()
        except TypeError:
            break
        print()
        print(output(read_json_file_6, sort, sort_order))


def write_json_file(x: list, filename: str) -> str:
    """
    Writing JSON file

    :param x: List that comes from one of the functions
    :type x: list
    :param filename: Name of the JSON file to write
    :type filename: str
    :return: Name of the JSON file
    :rtype: str
    """
    print("Writing JSON file...")
    json_str = json.dumps(x)
    with open(filename, "w") as file:
        file.write(json_str)
    return filename


def read_json_file(filename: str) -> list:
    """
    Reading JSON file

    :param filename: Name of the JSON file to read
    :type filename: str
    :return: Data from JSON file as a list
    :rtype: list
    """
    print("Reading JSON file...")
    with open(filename) as file:
        json_data = json.load(file)
    return json_data


def get_search_results(YOUTUBE, r=10000, m=50) -> list:
    """
    Per Youtube Data API docs:
    - returns a collection of search results that match the query parameters specified in the API request
    - each search.list API request costs 100 (Daily limit: 10k)

    :param YOUTUBE: Per Youtube Data API docs
    :type YOUTUBE: googleapiclient.discovery.Resource
    :param r: Number of iterations - the default is a high number (loop almost certainly won't reach this number,
    it will loop until there is no "nextPageToken" key, after which it will break, usually after cca 12 iterations)
    :type r: int
    :param m: Number of results per page (the default is 50 and it is also the maximum number)
    :type m: int
    :return: List of all the search results for "cs50p final project" query
    :rtype: list
    """
    print("Getting search results...")
    search_results = []
    token = []
    for i in tqdm(range(r), ncols=50, total=float("inf")):
        if i < 2:
            token_str = ",".join(token)
        else:
            token_str = token.pop(1)
        request = YOUTUBE.search().list(
            part="snippet", maxResults=m, pageToken=token_str, q="cs50p final project"
        )
        response = request.execute()
        try:
            token.append(response["nextPageToken"])
        except KeyError:
            break
        search_results.append(response)
    return search_results


def selected_search_results(x: list) -> list:
    """
    Appends relevant key-value pairs from 'search_results.json' to 'selected_search_results' list as dicts.

    :param x: List read from 'search_results.json'
    :type x: list
    :return: List of key-value pairs to be used in regex_check function
    :rtype: list
    """
    print("Getting IDs and Titles...")
    selected_search_results = []
    for i in tqdm(x, ncols=50):
        for k in i["items"]:
            try:
                selected_search_results.append(
                    {"videoId": k["id"]["videoId"], "title": k["snippet"]["title"]}
                )
            except KeyError:
                continue
    return selected_search_results


def regex_check(x: list) -> list:
    """
    Appends key-value pairs that passed regex check to a 'regex_check' list as dicts.

    :param x: List read from 'selected_search_results.json'
    :type x: list
    :return: List of key-value pairs that passed regex check
    :rtype: list
    """
    print("Regex check...")
    regex_check = []
    for i in tqdm(x, ncols=50):
        matches = re.search(
            r"(.*cs50.*(p |python).*final.*project.*)|(.*final.*project.*cs50.*(p |python).*)",
            i["title"],
            re.IGNORECASE,
        )
        if matches:
            regex_check.append(i)
        else:
            pass
    return regex_check


def get_video_ids(x: list) -> list:
    """
    Appends values of 'videoId' key (and removes duplicates as well) to a 'video_ids' list.

    :param x: List read from 'regex_check.json'
    :type x: list
    :return: List of values of 'videoId' key
    :rtype: list
    """
    print("Creating ID list...")
    video_ids = []
    for i in tqdm(x, ncols=50):
        video_ids.append(i["videoId"])
    video_ids = list(dict.fromkeys(video_ids))
    return video_ids


def get_video_stats(YOUTUBE, x: list) -> list:
    """
    Per Youtube Data API docs:
    - returns a list of videos that match the API request parameters
    - however, it's not possible to parse more than 50 video ids at once:
      for this reason, we're using a for loop (with step 50), slicing the list of video ids by 50
    - each video id API request costs 1 (Daily limit: 10k)

    :param YOUTUBE: Per Youtube Data API docs
    :type YOUTUBE: googleapiclient.discovery.Resource
    :param x: List read from 'video_ids.json'
    :type x: list
    :return: List of video stats
    :rtype: list
    """
    print("Getting video stats...")
    video_stats = []
    for i in tqdm(range(0, len(x), 50), ncols=50):
        request = YOUTUBE.videos().list(
            part="snippet,contentDetails,statistics", id=",".join(x[i : i + 50])
        )
        response = request.execute()
        video_stats.append(response)
    return video_stats


def final_data(x: list) -> list:
    """
    Appends relevant key-value pairs from 'video_stats.json' to 'final_data' list as dicts.

    :param x: List read from 'video_stats.json'
    :type x: list
    :return: List of final data, to be used for final output of the program
    :rtype: list
    """
    print("Getting final data...")
    final_data = []
    for i in tqdm(x, ncols=50):
        for k in i["items"]:
            template = {
                "Title": k.get("snippet").get("title"),
                "Description": k.get("snippet")
                .get("description")[:80]
                .replace("\n", " ")
                + "...",
                "Views": int(k.get("statistics").get("viewCount", 0)),
                "Likes": int(k.get("statistics").get("likeCount", 0)),
                "Comments": int(k.get("statistics").get("commentCount", 0)),
                "Published": k.get("snippet").get("publishedAt"),
                "YouTube Link": "https://www.youtube.com/watch?v=" + k.get("id"),
            }
            final_data.append(template)
    return final_data


def user_input() -> tuple:
    """
    User decides sorting type and sorting order.

    :return: Tuple containing str and bool to be used in 'output' function
    :rtype: tuple
    """
    print("-------------------------------------------------")
    try:
        while True:
            print("How would you like to sort the videos?")
            print()
            print("Usage: title, description, views, likes, comments, published")
            print()
            sort = input("Sort by: ")
            if (
                sort == "title"
                or sort == "description"
                or sort == "views"
                or sort == "likes"
                or sort == "comments"
                or sort == "published"
            ):
                sort = sort.capitalize()
                print("-------------------------------------------------")
                while True:
                    print("In what order would you like to sort the videos?")
                    print()
                    print("Usage: ascending, descending")
                    print()
                    sort_order = input("Sort order: ")
                    if sort_order == "ascending":
                        sort_order = False
                        return sort, sort_order
                    elif sort_order == "descending":
                        sort_order = True
                        return sort, sort_order
                    else:
                        print("-------------------------------------------------")
                        print("Invalid input!")
                        print()
                        continue
            else:
                print("-------------------------------------------------")
                print("Invalid input!")
                print()
                continue
    except EOFError:
        print("Exiting the program...")
        print()


def output(x: list, a: str, b: bool) -> str:
    """
    Outputting sorted final data using tabulate library.

    :param x: List read from 'final_data.json'
    :type x: list
    :param a: String from 'user_input' function, that defines sort type in 'sorted' function
    :type a: str
    :param b: Boolean from 'user_input' function, that defines sort order in 'sorted' function
    :type b: bool
    :return: Tabulate function as a string
    :rtype: str
    """
    index = range(1, (len(x) + 1))
    return tabulate(
        sorted(x, key=lambda s: s[a], reverse=b), showindex=index, headers="keys"
    )


if __name__ == "__main__":
    main()
