# CS50P Final Projects YouTube Database

#### Video Demo: https://www.youtube.com/watch?v=XoE0fZcFZUI

## Description

#### Intro

After finishing all the CS50P problem sets, I had no idea what kind of final project I should do. The only thing that seemed plausible to me was that it should be a program that solves a particular problem. And if possible, a problem not only mine.

But what kind of a problem?

Knowing that one of the requirements for the final project was a YouTube video, I went there for inspiration. Unfortunately, I was not very pleased with how YouTube handled "cs50p final project" query: many videos were not related to the final project, I was not happy with the sorting options, and most importantly, there was no way to get a top-down view of all the projects uploaded to YouTube.

Then I went to the CS50P Discord community and noticed that other members have the same issue: since there was no final projects gallery for CS50P, they also struggled to find inspiration for their final project.

However, one of the members posted a link to a [YouTube video](https://www.youtube.com/watch?v=bp0aS67imes) of a quite impressive final project that used YouTube API to search for and download Spotify songs.

And then, I got the idea!

> CS50P Final Projects YouTube Database

#### How it works

CS50P Final Projects YouTube Database is a CLI program that works as follows:

1. [Gets all the search results using YouTube API](https://developers.google.com/youtube/v3/docs/search/list?apix=true) for "cs50p final project" query
2. Uses regex `(.*cs50.*(p |python).*final.*project.*)|(.*final.*project.*cs50.*(p |python).*)` to filter out titles not matching the query
3. [Gets all the video stats using YouTube API](https://developers.google.com/youtube/v3/docs/videos/list?apix=true) of all the videos filtered by regex
4. Makes a final JSON file of all the videos with selected video stats
5. Outputs the final JSON file to a terminal using [tabulate library](https://pypi.org/project/tabulate/) with the user inputting sort type and sort order

#### Files and libraries

The program consists of two files: `project.py` and `test_project.py`.
`project.py` contains 11 functions (`main()` included).
`test_project.py` contains 6 tests.

After executing `project.py`, multiple JSON files are created. This is useful in a scenario where users might not want to make repeated API queries since they are quite 'expensive': one execution of the program 'costs' cca 1600 API queries: the daily quota is 10k, per Youtube Data API docs.

Users can comment out part of the code that makes API calls and execute the program using only the data in the JSON file(s).

Third-party libraries used:

- `google_api_python_client==2.90.0`
- `tabulate==0.9.0`
- `tqdm==4.65.0`

#### Next steps

Possible next steps for further improvement of the program:

- Make an option for executing the program without API calls if JSON files already exist (so there's no need to comment out the code)
- Include other video stats in the final output
- Make a GUI
