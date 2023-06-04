import requests
import json
from abc import ABC, abstractmethod


class HeadHunterAPI(ABC):

    @abstractmethod
    def get_total_pages(self, target: str) -> int:
        pass

    @abstractmethod
    def get_page(self, target: str, page: int):
        pass


class EmployerSearch(HeadHunterAPI):

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = "https://api.hh.ru/employers"
        # Initial parameters for the search query
        self.__params = {
            'area': '113',  # location - Russia
            'page': 0,  # page number
            'text': '',
            'per_page': 100,  # 100 vacancies per page
            'type': 'company',  # search only company
            'only_with_vacancies': True,  # at lest one vacancy per company
        }

    def get_total_pages(self, search_text: str) -> int:
        """
        Returns total number of pages for search query
        """
        # Update search parameters
        self.__params.update({'text': search_text, 'page': 0})
        # Get response
        response = requests.get(self.__base_url, self.__params)
        # Convert response to JSON object
        json_obj = json.loads(response.text)

        return json_obj['pages']

    def get_page(self, search_text: str,
                 page: int) -> list[tuple[str, str, str]]:
        """
        Returns a list of employers based on the search text
        """
        # Update search parameters
        self.__params.update({'text': search_text, 'page': page})
        # Get first response
        response = requests.get(self.__base_url, self.__params)
        # Convert response to JSON object
        json_obj = json.loads(response.text)
        # Get employer data from JSON object
        employers = self.retrieve_info(json_obj['items'])

        return employers

    @staticmethod
    def retrieve_info(items: list[dict]) -> list:
        """
        Retrieves HeadHunter ID, name and URL for each company from the list
        """
        employers = []
        for item in items:
            employers.append((item['id'], item['name'], item['alternate_url']))
        return employers


class VacancySearch(HeadHunterAPI):
    @staticmethod
    def get_exchange_rates() -> dict:
        """
        Returns exchange rates from API service
        """
        # Get response
        response = requests.get("https://api.hh.ru/dictionaries")
        # Convert to JSON object
        json_obj = json.loads(response.text)
        # Get currency list
        currencies = json_obj['currency']
        # Get exchange rates
        rates = {}
        for currency in currencies:
            rates[currency['code']] = currency['rate']
        return rates

    def __init__(self):
        """
        Initialise the class
        """
        self.__base_url = "https://api.hh.ru/vacancies"
        # Initial parameters for the search query
        self.__params = {
            'area': '113',  # location - Russia
            'page': 0,  # page number
            'per_page': 100,  # 100 vacancies per page
            'employer_id': '',  # HeadHunter ID of company
            'only_with_salary': True,  # only vacancies with salary
        }
        self.__rates = self.get_exchange_rates()

    def get_total_pages(self, employer_id: str) -> int:
        """
        Returns total number of pages for vacancies of employer
        """
        # Update search parameters
        self.__params.update({'employer_id': employer_id, 'page': 0})
        # Get response
        response = requests.get(self.__base_url, self.__params)
        # Convert response to JSON object
        json_obj = json.loads(response.text)

        return json_obj['pages']

    def get_page(self, employer_id: str,
                 page: int) -> list[tuple[str, int, str]]:
        """
        Returns a list of employers based on the search text
        """
        # Update search parameters
        self.__params.update({'employer_id': employer_id, 'page': page})
        # Get response
        response = requests.get(self.__base_url, self.__params)
        # Convert response to JSON object
        json_obj = json.loads(response.text)
        # Get vacancies data from JSON object
        vacancies = self.retrieve_info(json_obj['items'])
        return vacancies

    def retrieve_info(self, items: list[dict]) -> list[tuple[str, int, str]]:
        """
        Retrieves Name, Salary and URL for each vacancy from the list
        """
        vacancies = []
        for item in items:
            salary = self.get_salary(item)
            vacancies.append((item['name'], salary, item['alternate_url']))
        return vacancies

    def get_salary(self, vacancy: dict) -> int:
        """
        Determines the vacancy salary
        :param vacancy: Vacancy object from API
        """
        # Check if vacancy has minimum salary otherwise return maximum
        if vacancy['salary']['from'] is None:
            return int(vacancy['salary']['to'] /
                       self.__rates[vacancy['salary']['currency']])
        return int(vacancy['salary']['from'] /
                   self.__rates[vacancy['salary']['currency']])
