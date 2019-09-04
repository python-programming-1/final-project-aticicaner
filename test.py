import requests
import os

from bs4 import BeautifulSoup
from time import sleep

fuel_economy = 'https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1=2016&year2=2016&make=honda&baseModel=accord&srchtyp=ymm'

res = requests.get(fuel_economy)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'html.parser')
select = soup.select('div .panel-body')[0].find('td', class_ = 'mpg-comb')
sleep(1)

for i in select:
    print(i.string)
    print(type(str(i)))