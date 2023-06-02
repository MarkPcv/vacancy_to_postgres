import requests
import json

BASE_URL = 'https://api.hh.ru/'


def get_employers(search_text: str) -> list[tuple[str, str]]:
    """
    Returns a list of employers based on the search text
    """
    # Initial parameters for the search query
    params = {
        'area': '113',  # location - Russia
        'page': 0,  # page number
        'text': search_text,
        'per_page': 100,  # 100 vacancies per page
        'type': 'company',  # search only company
        'only_with_vacancies': True,  # at lest one vacancy per company
    }
    # Get first response
    response = requests.get("https://api.hh.ru/employers", params)
    # Convert response to JSON object
    json_obj = json.loads(response.text)
    employers = retrieve_employers(json_obj['items'])
    # Get total number of pages
    pages = json_obj['pages']
    # Get remaining employers information
    for page in range(1, pages):
        params['page'] = page
        response = requests.get("https://api.hh.ru/employers", params)
        json_obj = json.loads(response.text)
        employers.extend(retrieve_employers(json_obj['items']))

    return employers


def retrieve_employers(items: list[dict]) -> list[tuple[str, str]]:
    """
    Retrieves HeadHunter ID and name for each company from the list
    """
    employers = []
    for item in items:
        employers.append((item['id'], item['name']))
    return employers

# TESTING
# result = get_employers('1')
# print(result)
# print(len(result))
