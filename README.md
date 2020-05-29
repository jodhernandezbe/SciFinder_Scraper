# SciFinder_Scraper
This is a Python script which uses Selenium for scraping CAS SciFinder and finding prices for chemical substances.

## Requirements

In order to use this code you kneed the following requirements:

1. A password and an username on SciFinder (https://accounts.cas.org/products/)
2. Google Chrome installed in your computer. However, you can modify the code and use other selenium driver (e.g., Firefox)
3. A .csv with a column named CAS NUMBER
4. Install:
   - selenium (https://pypi.org/project/selenium/)
   - webdriver_manager (https://pypi.org/project/webdriver-manager/)
   - pandas (https://pypi.org/project/pandas/)
   - regex (https://pypi.org/project/regex/)
   - argparse (https://pypi.org/project/argparse/)

## Use

To run the code from the Linux/Ubuntu terminal or Windows CMD:

1. You must move to the folder where is SciFinder_Scapper.py
2. Use: python SciFinder_Scapper.py -FR *file_path_to_read_CAS* -FS *file_path_to_save_infomartion* -P *YourPassword* -U *YourUser*
