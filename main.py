from services.api_service import *


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


def chose_employers_by_user() -> list[tuple[str, str]]:
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


def main():
    """
    Main Algorithm
    """
    print("Greetings, let's start employers' search!")
    # Ask user to choose 10 employers
    result = chose_employers_by_user()
    print(result)


if __name__ == "__main__":
    main()
