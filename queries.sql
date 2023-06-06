-- Create and remove database
DROP DATABASE database_name;
CREATE DATABASE database_name;

-- Create Employers table
CREATE TABLE employers(
    id SERIAL PRIMARY KEY,
    company_name VARCHAR,
    headhunter_id INTEGER,
    url VARCHAR
);

-- Create Vacancies table
CREATE TABLE vacancies(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    company_id INTEGER,
    salary INTEGER,
    url VARCHAR
);

-- Fill Employers table and return primary key
INSERT INTO employers(company_name, headhunter_id, url)
VALUES ('Company_Name', 'HeadHunter_ID', 'Employer_URL')
RETURNING id;

-- Fill Vacancies table
INSERT INTO vacancies(name, company_id, salary, url)
VALUES ('Vacancy_Name', 'Employer_ID', 'Salary', 'Vacancy_URL');

-- Create relationship between Employers and Vacancies tables
ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_company
FOREIGN KEY(company_id) REFERENCES employers(id);

-- Database Manager Class Queries
-- Get employers and the number of vacancies
SELECT employers.company_name, COUNT(vacancies.id)
FROM employers
JOIN vacancies ON vacancies.company_id = employers.id
GROUP BY employers.company_name;

-- Get all vacancies
SELECT employers.company_name, vacancies.name, vacancies.salary, vacancies.url
FROM vacancies
JOIN employers ON vacancies.company_id = employers.id;

-- Get average salary
SELECT AVG(salary) FROM vacancies;

-- Get vacancies with salaries above average
SELECT employers.company_name, vacancies.name, vacancies.salary, vacancies.url
FROM vacancies
JOIN employers ON vacancies.company_id = employers.id
WHERE vacancies.salary >= (SELECT AVG(salary)
FROM vacancies);

-- Get vacancies with keyword
SELECT *
FROM vacancies
WHERE name ILIKE '%Keyword%'

