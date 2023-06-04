from sql_service import *


class DBManager:
    def __init__(self, db_name: str):
        self.params = config()
        self.params.update({'dbname': db_name})

    def get_companies_and_vacancies_count(self):
        """
        Get the list of companies and number of their vacancies
        """
        result =[]
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    # Create Employers Table
                    cur.execute("""
                        SELECT employers.company_name, COUNT(vacancies.id)
                        FROM employers
                        JOIN vacancies ON vacancies.company_id = employers.id
                        GROUP BY employers.company_name 
                    """)
                    result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result

    def get_all_vacancies(self):
        """
        Get the list of all vacancies
        """
        result = []
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    # Create Employers Table
                    cur.execute("""
                        SELECT employers.company_name, vacancies.name, 
                        vacancies.salary, vacancies.url
                        FROM vacancies
                        JOIN employers ON vacancies.company_id = employers.id
                    """)
                    result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result

    def get_avg_salary(self):
        """
        Get the average salary of all vacancies
        """
        result = []
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    # Create Employers Table
                    cur.execute("""
                        SELECT AVG(salary)
                        FROM vacancies
                    """)
                    result = cur.fetchone()[0]
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result

    def get_vacancies_with_higher_salary(self):
        """
        Get list of vacancies with salary above average
        """
        result = []
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    # Create Employers Table
                    cur.execute("""
                        SELECT employers.company_name, vacancies.name, 
                        vacancies.salary, vacancies.url
                        FROM vacancies
                        JOIN employers ON vacancies.company_id = employers.id
                        WHERE vacancies.salary >= (SELECT AVG(salary) 
                        FROM vacancies)
                    """)
                    result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """
        Get list of vacancies that match keyword
        """
        result = []
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    # Create Employers Table
                    cur.execute(
                        f"""
                        SELECT *
                        FROM vacancies
                        WHERE name ILIKE '%{keyword}%'
                        """
                    )
                    result = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return result
