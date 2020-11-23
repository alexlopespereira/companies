import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import shutil

from util import wait_element
from auth_data import email, password

class crawler():

    def __init__(self, download_dir, dest_dir):
        self.download_dir = download_dir
        self.dest_dir = dest_dir
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self.download_dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        fp.set_preference("pdfjs.disabled", True)
        self.driver = webdriver.Firefox(firefox_profile=fp)


    def search_funding(self, threshold, start_announced, end_announced, start_founded, end_founded):
        # self.driver.get(url)
        dates_announced = pd.date_range(start=start_announced, end=end_announced, freq="6M")
        status = wait_element(self.driver, "//search-date//input[@type='search']", by=By.XPATH, to_sleep=5)
        ins_search = self.driver.find_elements_by_xpath("//search-date//input[@type='search']")
        for sa, ea in zip(dates_announced[0:-1], dates_announced[1:]):
            # status = wait_element(self.driver, "//input[@type='search']", by=By.XPATH)
            in_start_announced = ins_search[0]
            in_start_announced.clear()
            in_start_announced.send_keys(sa.strftime("%Y/%m/%d"))
            in_end_announced = ins_search[1]
            in_end_announced.clear()
            in_end_announced.send_keys(ea.strftime("%Y/%m/%d"))
            dates_founded = pd.date_range(start=start_founded, end=end_founded, freq="6M")
            for sf, ef in zip(dates_founded[0:-1], dates_founded[1:]):
                in_start_founded = ins_search[2]
                in_start_founded.clear()
                in_start_founded.send_keys(sf.strftime("%Y/%m/%d"))
                in_end_founded = ins_search[3]
                in_end_founded.clear()
                in_end_founded.send_keys(ef.strftime("%Y/%m/%d"))
                wait_element(self.driver, '//button[@aria-label="Search"]', by=By.XPATH, to_sleep=2)
                button_searc = self.driver.find_element_by_xpath('//button[@aria-label="Search"]')
                button_searc.click()
                wait_element(self.driver, '//div[@class="cb-overflow-ellipsis"]', by=By.XPATH, to_sleep=1)
                nresults = int(self.driver.find_element_by_xpath("//results-info[@class='flex-none hide show-gt-xs']/h3").text.split(" ")[-2].replace(",", ""))
                if nresults > threshold:
                    print(f"{sa.strftime('%Y/%m/%d')}, {ea.strftime('%Y/%m/%d')}, {sf.strftime('%Y/%m/%d')}, {ef.strftime('%Y/%m/%d')}. {nresults} > {threshold}")
                elif nresults > 0:
                    wait_element(self.driver, '//div[@class="cb-overflow-ellipsis"]', by=By.XPATH)
                    button_export = self.driver.find_element_by_xpath('//export-csv-button//button')
                    button_export.click()
                    today_str = datetime.datetime.today().strftime("%m-%d-%Y")
                    filename = f"{self.download_dir}/{self.search_name}-{today_str}.csv"
                    while not os.path.exists(filename):
                        time.sleep(1)

                    dest_file = f"{self.dest_dir}/{self.search_name}_{sa.strftime('%Y%m%d')}_{ea.strftime('%Y%m%d')}_{sf.strftime('%Y%m%d')}_{ef.strftime('%Y%m%d')}.csv"
                    shutil.move(filename, dest_file)

    def search_startup(self, threshold, start_founded, end_founded):
        dates_founded = pd.date_range(start=start_founded, end=end_founded, freq="1M")
        status = wait_element(self.driver, "//search-date//input[@type='search']", by=By.XPATH, to_sleep=5)
        ins_search = self.driver.find_elements_by_xpath("//search-date//input[@type='search']")
        for sa, ea in zip(dates_founded[0:-1], dates_founded[1:]):
            in_start_announced = ins_search[0]
            in_start_announced.clear()
            in_start_announced.send_keys(sa.strftime("%Y/%m/%d"))
            in_end_announced = ins_search[1]
            in_end_announced.clear()
            in_end_announced.send_keys(ea.strftime("%Y/%m/%d"))
            wait_element(self.driver, '//button[@aria-label="Search"]', by=By.XPATH, to_sleep=2)
            button_search = self.driver.find_element_by_xpath('//button[@aria-label="Search"]')
            button_search.click()
            wait_element(self.driver, '//div[@class="cb-overflow-ellipsis"]', by=By.XPATH, to_sleep=1)
            nresults = int(self.driver.find_element_by_xpath("//results-info[@class='flex-none hide show-gt-xs']/h3").text.split(" ")[-2].replace(",", ""))
            if nresults > threshold:
                print(f"{sa.strftime('%Y/%m/%d')}, {ea.strftime('%Y/%m/%d')}. {nresults} > {threshold}")
            elif nresults > 0:
                wait_element(self.driver, '//div[@class="cb-overflow-ellipsis"]', by=By.XPATH)
                button_export = self.driver.find_element_by_xpath('//export-csv-button//button')
                button_export.click()
                today_str = datetime.datetime.today().strftime("%m-%d-%Y")
                filename = f"{self.download_dir}/{self.search_name}-{today_str}.csv"
                while not os.path.exists(filename):
                    time.sleep(1)

                dest_file = f"{self.dest_dir}/{self.search_name}_{sa.strftime('%Y%m%d')}_{ea.strftime('%Y%m%d')}.csv"
                shutil.move(filename, dest_file)

    def crawl(self, url, type="funding"):
        self.driver.get(url)
        self.search_name = type
        self.dest_dir = os.path.join(self.dest_dir, type)
        status = wait_element(self.driver, "//input[@id='mat-input-1']", by=By.XPATH)
        in_login = self.driver.find_element_by_xpath("//input[@id='mat-input-1']")
        in_login.send_keys(email)
        in_pass = self.driver.find_element_by_xpath("//input[@id='mat-input-2']")
        in_pass.send_keys(password)
        wait_element(self.driver, '//button[contains(@class,"login")]', by=By.XPATH)
        button_login = self.driver.find_element_by_xpath('//button[contains(@class,"login")]')
        button_login.click()
        if type == "funding":
            self.search_funding(1000, "2015/01/01", "2020/01/01", "2015/01/01", "2018/01/01")
        elif type == "startups":
            self.search_startup(1000, "2006/01/01", "2019/06/01")


if __name__ == '__main__':
    url_funding = 'https://www.crunchbase.com/lists/fundingrounds/be3ae454-0bc6-443a-8f57-e29f3c3c7f09/funding_rounds'
    url_startup = "https://www.crunchbase.com/lists/startups/8d54f127-8d3e-4a1b-ade7-bfbaaa5bfc97/organization.companies"
    search_name = "funding-rounds"
    dest_dir = "/home/alex/vscode/data/original/crunchbase/"
    download_dir = "/home/alex/vscode/data/original/crunchbase/tmp"
    obj = crawler(download_dir=download_dir, dest_dir=dest_dir)
    # obj.crawl(url_funding, type="funding")
    obj.crawl(url_startup, type="startups")

