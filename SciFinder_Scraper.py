#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import re
import argparse


def extract_data(browser):
    regex = r'[0-9]+\.?[0-9]*\s?[A-Za-z]+\s?\,\s?[A-Z]{3}\s?[0-9]+\.?[0-9]*'
    elements = dynamic_wait(browser, '//div[@class="quantity-price ng-star-inserted"]', Price = True)
    if elements:
        Prices = [tuple([p.text,
                     p.find_element_by_xpath('../preceding-sibling::div[1]').text,
                     p.find_element_by_xpath('../preceding-sibling::div[3]//a[@class="company-name"]').text,
                     p.find_element_by_xpath('../preceding-sibling::div[3]//div[@class="country-name"]').text])
                 for p in  elements if re.search(regex, p.text)]
    else:
        Prices = [tuple([None, None, None, None])]
    return Prices


def dynamic_wait(browser, path, click = False, send = False, chem =  None, Price = False, clear = False, Count = False):
    delay = 30
    try:
        element = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, path)))
        if click:
            element.click()
        elif send:
            element.send_keys(chem)
            browser.find_element_by_xpath('//button[@class="btn btn-primary btn-search qa-tooltip"]').click()
        elif Price:
            element = browser.find_elements_by_xpath(path)
            return element
        elif clear:
            element.clear()
        elif Count:
            return int(re.sub(r'\,', '', element.text))
    except TimeoutException:
        dynamic_wait(browser, '//input[@name="textQuery"]', clear = True)
        pass


def Browsing(Chemicals, File_save, YourUsername, Pa55worD):
    options = Options()
    options.headless = True
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument('--verbose')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--log-level=3")
    options.add_argument('--hide-scrollbars')
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
    browser.get('https://accounts.cas.org/products/')
    Options_search = browser.find_elements_by_xpath('//select[@id="product"]/option')
    for Option_search in Options_search:
        if Option_search.text == 'SciFinderⁿ':
            Option_search.click()
            break
    dynamic_wait(browser, '//button[@id="next-btn"]', click = True)
    username = browser.find_element_by_xpath('//input[@id="username"]')
    password = browser.find_element_by_xpath('//input[@id="password"]')
    username.send_keys(YourUsername)
    password.send_keys(Pa55worD)
    browser.find_element_by_xpath('//button[@id="loginButton"]').click()
    dynamic_wait(browser, '//label[@for="result-type-commercial"]', click = True)
    Searching_chemicals(browser, Chemicals, File_save)


def Searching_chemicals(browser, Chemicals, File_save):
    df = pd.DataFrame()
    print('-' * 45)
    print('{:15s} {:15s} {:15s}'.format('CAS Number', '# supplier(s)', '# price(s)'))
    print('-' * 45)
    for chem in Chemicals:
        dynamic_wait(browser, '//input[@name="textQuery"]', send = True, chem = chem)
        N_results = dynamic_wait(browser, '//span[@class="results-count"]', Count = True)
        if N_results != 0:
            Prices = extract_data(browser)
            try:
                browser.find_element_by_xpath('//ul[@class="pagination"]')
                xpath1 = '//li[@class="direction-link next ng-star-inserted"]/preceding-sibling::li[1]/a'
                xpath2 = '//li[@class="direction-link next ng-star-inserted"]/preceding-sibling::li[1]/span'
                Number_of_pages = int(re.sub('\,', '', browser.find_element_by_xpath('{} | {}'.format(xpath1, xpath2)).text))
                for j in range(Number_of_pages - 1):
                    dynamic_wait(browser, "//a/span[contains(text(),'Next')]", click = True)
                    Prices = Prices + extract_data(browser)
            except NoSuchElementException:
                Prices = Prices
            print('{:15s} {:15s} {:15s}'.format(chem, str(N_results), str(len(Prices))))
        else:
            print('{:15s} {:15s} {:15s}'.format(chem, 'No found', 'No found'))
            Prices = [tuple(['No found, No found', 'Not found', 'Not found', 'Not found'])]
        df_aux = pd.DataFrame(Prices, columns =['PRICE', 'PURITY', 'COMPANY_NAME', 'COUNTRY'])
        df_aux['CAS NUMBER'] = chem
        df = pd.concat([df, df_aux], ignore_index = True, sort = True, axis = 0)
        del df_aux, Prices
        dynamic_wait(browser, '//input[@name="textQuery"]', clear = True)
    browser.close()
    df[['QUANTITY','PRICE']] = df.PRICE.str.split(',', expand = True)
    df['CURRENCY'] = df['PRICE'].str.extract('([a-zA-Z\s]+)', expand = True)
    df['CURRENCY'] = df['CURRENCY'].str.strip()
    df['PRICE'] = df['PRICE'].str.extract('([0-9]+\.?[0-9*])', expand = True)
    df['PRICE'] = df['PRICE'].where(pd.notnull(df['PRICE']), 'Not found')
    df.to_csv(File_save, sep = ',', index = False)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(argument_default = argparse.SUPPRESS)

    parser.add_argument('-FR', '--Reading_file_path', nargs = '+',
                        help = 'Enter the file(s) with the CAS NUMBER.',
                        type = str)

    parser.add_argument('-FS', '--Saving_file_path',
                        help = 'Enter the path for the file with the database.',
                        required = True)

    parser.add_argument('-P', '--Password',
                        help = 'Enter your password SciFinder.',
                        type = str)

    parser.add_argument('-U', '--User',
                        help = 'Enter your username SciFinder.',
                        type = str)

    args = parser.parse_args()

    Chemicals = list()
    for file in args.Reading_file_path:
        df_chemicals = pd.read_csv(file, usecols = ['CAS NUMBER'])
        df_chemicals = df_chemicals.loc[~df_chemicals['CAS NUMBER'].str.contains(r'[A-Z]')]
        df_chemicals['CAS NUMBER'] = df_chemicals['CAS NUMBER'].str.replace(r'\-', '')
        Chemicals = Chemicals + df_chemicals['CAS NUMBER'].tolist()
    del df_chemicals
    Chemicals = list(set(Chemicals))

    File_save = args.Saving_file_path
    YourUsername = args.User
    Pa55worD = args.Password
    Browsing(Chemicals, File_save, YourUsername, Pa55worD)
