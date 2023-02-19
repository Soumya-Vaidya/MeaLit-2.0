#to scrape images from zomato db to store into TextFil.txt

from lib2to3.pgen2 import driver
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd 
chrome_driver_path = "C:/Users/anush/Downloads/Development/chromedriver.exe"
driver= webdriver.Chrome(executable_path=chrome_driver_path)

# driver.get("https://amazon.in")

# print(src)
file1 = open("TextFile.txt","a")

df=pd.read_csv('zomato final scraping.csv')
i=0
for links in df['URL']:
    print(links)
    driver.get(links)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    images = soup.find_all('img')
    # images = images[2].get('src')
    print("-------------------------------------")
    #df//['IMAGES'][i] = images[2]['src']
    file1.write(images[2]['src'])
    file1.write("\n")
    print(images[2]['src'])
    i+=1
    # driver.close()
    # df.to_csv('zomato scraped.csv')
    # print(images[2]['src'])
    # for item in images:
    #  print(item['src'])
file1.close()