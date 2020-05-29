# SciFinder_Scraper
This is a Python script which uses packages such as Selenium and Pandas for scraping CAS SciFinder and finding prices for chemical substances.

In order to use this code you kneed the following requirements:

1. A password and an username on SciFinder (https://accounts.cas.org/products/)
2. Google Chrome installed in your computer. However, you can modify the code and use other selenium driver (e.g., Firefox)
3. A .csv with a column named CAS NUMBER
4. Install:
   4.1. selenium (https://pypi.org/project/selenium/)
   4.2. webdriver_manager (https://pypi.org/project/webdriver-manager/)
   4.3. pandas (https://pypi.org/project/pandas/)
   4.4. regex (https://pypi.org/project/regex/)
   4.5. argparse (https://pypi.org/project/argparse/)

To run the code:
1. You must move to the folder where is SciFinder_Scapper.py
2. Use: python SciFinder_Scapper.py -FR file_path_to_read_CAS -FS file_path_to_save_infomartion -P YourPassword -U YourUser
