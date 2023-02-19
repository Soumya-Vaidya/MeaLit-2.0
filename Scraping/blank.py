#used to scrape blank entr

from lib2to3.pgen2 import driver
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
chrome_driver_path = "C:/Users/anush/Downloads/Development/chromedriver.exe"
driver= webdriver.Chrome(executable_path=chrome_driver_path)

file1 = open("blank.txt","a")

df=pd.read_csv('blank.csv')
i=0
for links in df['URL']:
    print(links)
    driver.get(links)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    images = soup.find_all('img')
    print("-------------------------------------")
    file1.write(images[2]['src'])
    file1.write("\n")
    print(images[2]['src'])
    i+=1
file1.close()