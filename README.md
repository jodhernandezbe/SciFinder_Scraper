# SciFinder_Scraper

This is a Python script which uses Selenium for scraping CAS SciFinder<sup>n</sup> and extracting prices and suppliers and their locations for chemical substances.

## Requirements

In order to use this code you kneed the following requirements:

1. A password and an username on SciFinder<sup>n</sup> (https://accounts.cas.org/products/)
2. Google Chrome installed in your computer. However, you can modify the code and use other selenium driver (e.g., Firefox)
3. A .csv with a column named as CAS NUMBER
4. Install:
   - selenium (https://pypi.org/project/selenium/)
   - webdriver_manager (https://pypi.org/project/webdriver-manager/)
   - pandas (https://pypi.org/project/pandas/)
   - regex (https://pypi.org/project/regex/)
   - argparse (https://pypi.org/project/argparse/)

## How to use

To run the code from the Linux/Ubuntu terminal or Windows CMD:

1. You must move to the folder where is SciFinder_Scapper.py
2. Run the following command: 

```
   python SciFinder_Scapper.py -FR file_path_to_read_CAS -FS file_path_to_save_infomartion -P YourPassword -U YourUser
```
   - file_path_to_read_CAS: path of the file with the CAS numbers to search for.
   - file_path_to_save_infomartion: path of the file that you will used to save the information.
   - YourPassword: your password in SciFinder<sup>n</sup>.
   - YourUser: your user registed in SciFinder<sup>n</sup>

## Output

You will obtain a .csv file with the following columns:

| Column name | Description |
| ------------- | ------------- |
| CAS NUMBER | CAS number for the chemical |
| COMPANY NAME | Chemical supplier |
| COUNTRY | Country where the supplier is located |
| PRICE | Price and currency in which the chemical is sold by the supplier |
| PURITY | Purity in which the chemical is offered by the supplier |
| QUANTITY | Quantity and unit in which the chemical is sold by the supplier |
