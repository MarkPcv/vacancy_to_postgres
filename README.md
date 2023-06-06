# Database Workflow using API

## Project Description
This project allows user to create Database with tables: **Employers** 
and **Vacancies**. The information about employers and vacancies is gathered
using **HeadHunter** API platform which is commonly used in CIS region. User 
selects employers and their vacancies are stored in the user-defined database.
Then user is given a list of commands through which information from the 
database can be retrieved.

The search criteria are the following:

- Search only includes employers and their vacancies in _Russian Federation_
- Employer without open vacancies are not displayed
- Only **company-type** employers are displayed
- Vacancies without salary are ignored and only _minimum_ salary is taken into 
account and displayed to user. _Maximum_ salary is shown if minimum is omitted.
- If vacancy's salary is not given in rubles (RUB), its salary will be 
converted to RUB using exchange rate provided by API.

---
## Installation and Run

Use the package manager **poetry** to install all necessary packages:
```bash
poetry install
```
Run poetry script to **start** the program using Terminal (or just run main.py)
```bash
poetry run start
```

---
## Simple Algorithm

The simple high-level algorithm of the program is described below:
1. User greeting
2. Employer selection (10 companies must be chosen)
   1. User search query
   2. Presentation of each employer
   3. Employer choice
3. Database creation
4. Tables creation
5. Tables entries
   1. Employers table entry
   2. Vacancy search
   3. Vacancies table entry
   4. Establishment of tables' relationship
6. Information manipulation using several commands
7. Exit


---
## Tech Stack
<img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/postgresql-blue?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/GIT-blue?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/Poetry-blue?style=for-the-badge&logo=poetry&logoColor=white" />
