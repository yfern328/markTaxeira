##### **markTaxiera: The Fantasy Baseball Keeper Tax Solution**

Authors: Yelstin Fernandes & Justin Ramos

________________________________________________________________________________


### **Description**

This python program does two tasks:

1) This python program loads fantasy baseball player projections from a custom E S P N,
league, saves the data in a JSON file, and then parses it into a CSV for the purposes
of conducting an offline draft due to limited E S P N keeper draft features.
[written by Yelstin Fernandes]

*packages used: python-dotenv, selenium, beautifulsoup4, pandas* 

**samples of output can be viewed in ./temp**


2) This python program will load transaction logs for teams in an E S P N
fantasy baseball league. The program will facilitate the usage of a keeper tax
system for private and offline usage to augment limited E S P N draft features.
[to be built by Yelstin Fernandes & Justin Ramos]

This program was built on MacOS using:
  -Python 3.8
  -Google Chrome Version 88.0
  -ChromeDriver 88
    [https://sites.google.com/a/chromium.org/chromedriver/downloads]
    [https://chromedriver.storage.googleapis.com/index.html?path=88.0.4324.96/]


________________________________________________________________________________


### **Recommendations**

# Set up a virtual environment

It is recommended to build a virtual environment in the backend directory and
then use the 'requirements.txt' file to install required packages.

To create the virtual environment run:

  python3 -m venv venv

Next to activate the virtual environment run:

  source venv/bin/activate

**You can deactivate the virtual environment by running:

  deactivate

To install the requirements in the virtual environment run:

  pip install -r requirements.txt

To update the requirements.txt file run:

  pip freeze > requirements.txt

### **Set environment variables**

Additionally in settings it is necessary to update the .env file to have
proper connection strings
________________________________________________________________________________
