from services.api_service import *
from services.sql_service import *


def get_employer_choice(employer_name: str) -> int:
    """
    Asks user: to save the employer to the list or not
    """
    choice = int(input("Employer's information:\n"
                       f"Company name: {employer_name}\n"
                       "Would you like to add it to the list?\n"
                       "1 - Yes\n"
                       "0 - No\n"))
    # Validate user choice
    while choice not in range(0, 2):
        choice = int(input("Please enter correct number either 0 or 1: "))

    return choice


def get_employers(search_text: str) -> list:
    """
    Returns a list of employers based on the search query
    """
    # Create instance of Employer Search
    api_search = EmployerSearch()
    # Get total pages of the matching employers
    pages = api_search.get_total_pages(search_text)
    # Record all employers and return them
    employers = []
    for page in range(0, pages):
        employers.extend(api_search.get_page(search_text, page))
    return employers


def chose_employers_by_user() -> list[tuple[str, str, str]]:
    """
    Returns the list of employers chosen by user
    """
    chosen_employers = []
    chosen = False
    while not chosen:
        # Ask user to enter search text
        search_text = input("Please enter search query: ")
        # Get list of employers
        employers = get_employers(search_text)
        # Show information one by one
        for employer in employers:
            user_choice = get_employer_choice(employer[1])
            # Add employer to the list of interest
            if user_choice:
                chosen_employers.append(employer)
            # Exit loop when 10 employers found
            # TODO: CHANGE TO '10' IN CONDITION
            if len(chosen_employers) == 2:
                chosen = True
                break

    return chosen_employers


def fill_tables(employers: list, db_name: str) -> None:
    """
    Fills Employers and Vacancies tables
    """
    for employer in employers:
        # Insert information into Employers table and return its primary key
        pk_employer = insert_employer_data(employer, db_name)
        # Create instance of Vacancy Search
        api_search = VacancySearch()
        # Get employer ID
        employer_id = employer[0]
        # Get total number of pages for vacancies of each employer
        pages = api_search.get_total_pages(employer_id)
        # Get information from each page and fill into vacancies table
        for page in range(0, pages):
            # Get information about vacancies from one page
            vacancies = api_search.get_page(employer_id, page)
            # Fill the Vacancy table
            insert_vacancies_data(vacancies, pk_employer)


def main():
    """
    Main Algorithm
    """
    print("Greetings, let's start employers' search!")
    # Ask user to choose 10 employers
    employers = chose_employers_by_user()
    # Ask user to enter database name
    db_name = input("Please enter database name: ")
    # Create database
    create_database(db_name)
    # Create tables
    create_tables(db_name)
    # Store each employer and their vacancies into the tables
    fill_tables(employers, db_name)


if __name__ == "__main__":
    main()
