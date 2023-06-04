import psycopg2

from configparser import ConfigParser


def config(filename="database.ini", section="postgresql") -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section,
                                                               filename))
    return db


def create_database(db_name: str) -> None:
    """
    Creates a new database
    """
    # Get parameters from .ini file
    params = config()
    # Establish connection
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    # Create database
    try:
        cur.execute(f'DROP DATABASE {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')
    except psycopg2.Error:
        # In case where database was not created previously
        cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name: str) -> None:
    """
    Creates Employers and Vacancies tables
    """
    # Get parameters from .ini file
    params = config()
    params.update({'dbname': db_name})

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Create Employers Table
                cur.execute("""
                    CREATE TABLE employers(
                        id SERIAL PRIMARY KEY,
                        company_name VARCHAR,
                        headhunter_id INTEGER,
                        url VARCHAR
                    )
                """)
                # Create Vacancies Table
                cur.execute("""
                    CREATE TABLE vacancies(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR,
                        company_id VARCHAR,
                        salary INTEGER,
                        url VARCHAR
                    )
                """)
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_employer_data(employer: tuple, db_name: str) -> int:
    """
    Fills Employers table with data about employer
    """
    # Get parameters from .ini file
    params = config()
    params.update({'dbname': db_name})
    employer_id = 0
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Fill Employers Table
                cur.execute(
                    """
                    INSERT INTO employers(company_name, headhunter_id, url)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (employer[1], employer[0], employer[2])
                )
                # Get primary key fot current employer
                employer_id = cur.fetchone()[0]

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    # return primary key of current employer
    return employer_id


# TODO: SQL for Vacancy
def insert_vacancies_data(vacancies: list,
                          pk_employer: int, db_name: str) -> None:
    """
    Fills Vacancies table with data about vacancies
    """
    # Get parameters from .ini file
    params = config()
    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    # Fill Vacancies Table
                    cur.execute(
                        """
                        INSERT INTO vacancies(name, company_id, salary, url)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (vacancy[0], pk_employer, vacancy[1], vacancy[2])
                    )

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()