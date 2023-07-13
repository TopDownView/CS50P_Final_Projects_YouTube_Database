from project import (
    write_json_file,
    read_json_file,
    selected_search_results,
    regex_check,
    get_video_ids,
    final_data,
)


"""
All the tests are to be executed only after the JSON files are created.
"""


def test_write_json_file():
    assert write_json_file([1, 2, 3], "test_1.json") == "test_1.json"


def test_read_json_file():
    assert read_json_file("test_1.json") == [1, 2, 3]


def test_selected_search_results():
    assert selected_search_results(
        read_json_file("search_results.json")
    ) == read_json_file("selected_search_results.json")


def test_regex_check():
    assert regex_check(
        read_json_file("selected_search_results.json")
    ) == read_json_file("regex_check.json")


def test_get_video_ids():
    assert get_video_ids(read_json_file("regex_check.json")) == read_json_file(
        "video_ids.json"
    )


def test_final_data():
    assert final_data(read_json_file("video_stats.json")) == read_json_file(
        "final_data.json"
    )
