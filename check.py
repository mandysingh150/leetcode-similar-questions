from colorama import Back
import pandas as pd
import requests
import json

# Leetcode API URL to get json of problems on algorithms categories
ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

# Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
# If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

# Load JSON from API
algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
algorithms_problems_json = json.loads(algorithms_problems_json)

# List to store question_title_slug
links = []
for child in algorithms_problems_json["stat_status_pairs"]:
    # Only process free problems
    if not child["paid_only"]:
        question__title_slug = child["stat"]["question__title_slug"]
        question__article__slug = child["stat"]["question__article__slug"]
        question__title = child["stat"]["question__title"]
        frontend_question_id = child["stat"]["frontend_question_id"]
        difficulty = child["difficulty"]["level"]
        links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

# Sort by difficulty followed by problem id in ascending order
links = sorted(links, key=lambda x: x[2])

df1 = pd.read_csv('./data.csv')
df2 = pd.DataFrame(links, columns=['question__title_slug', 'difficulty', 'frontend_question_id', 'question__title', 'question__article__slug'])

if df1['frontend_question_id'].all() == df2['frontend_question_id'].all():
    print(Back.GREEN + 'All non-premium questions are present' + Back.BLACK)
else:
    print(Back.RED + 'Some non-premium questions are NOT present\n' + Back.BLACK)