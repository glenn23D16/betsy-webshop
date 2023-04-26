# Betsy-webshop

Betsy is a fictional web marketplace where people can sell homemade goods. This project tests skills in modeling data as well as using the peewee ORM.

**Requirements**

Python 3
peewee
Whoosh
Installation

Clone the repository: git clone https://github.com/glenn23d16/betsy-webshop.git
Change directory to the project folder: cd betsy-webshop
Create and activate a virtual environment: python3 -m venv venv and source venv/bin/activate on Mac/Linux or venv\Scripts\activate on Windows
To install the required dependencies, run the following command: pip3 install -r requirements.txt

**Usage**

To start the program, run python3 main.py from the command line. The program will prompt you to choose from a list of options.

**Testing**

To run the tests, run python3 test_betsy.py from the command line. Note that the tests will use and modify the existing `betsy.db` database. Make sure to backup your data before running the tests.

**Search Functionality**

The Betsy webshop has a search function that allows users to search for products based on a keyword or phrase. The search functionality targets both the name and description fields of the products and is case-insensitive. The products are indexed, which minimizes the time spent on querying them. Additionally, the search function accounts for spelling mistakes made by users and returns products even if a spelling error is present.
