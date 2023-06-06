from services.utils import *


def main():
    """
    Main Algorithm
    """
    print("Greetings, let's start employers' search!")
    # Ask user to choose 10 employers
    employers = chose_employers_by_user()
    # Ask user to enter database name
    db_name = input("\nEnter database name: ")
    # Create database
    create_database(db_name)
    # Create tables
    create_tables(db_name)
    # Store each employer and their vacancies into the tables
    fill_tables(employers, db_name)
    # Get information from tables based on user preferences
    use_db_manager(db_name)


if __name__ == "__main__":
    main()
