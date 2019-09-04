import requests
import os

from bs4 import BeautifulSoup
from time import sleep

# sample_url = 'https://losangeles.craigslist.org/search/cto?auto_make_model=honda+accord&min_auto_year=2016&max_auto_year=2019'
# fuel_economy = 'https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1=2016&year2=2016&make=Volkswagen&baseModel=Passat&srchtyp=ymm'

craigslist_short = 'https://losangeles.craigslist.org/search/cto?auto_make_model='
fuel_short = 'https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1='

#cars to look up
cars = {'honda' : ['accord', 'civic'], \
    'audi' : ['a3', 'a4'], \
    'volkswagen' : ['passat', 'jetta'], \
    'toyota' : ['prius', 'corolla']}

min_year = '2016'
max_year = '2016'

insurance_cost = 849 #average in california

car_data = {} # this is the main dictionary to keep information in

for car_make in cars:
    for car_model in cars[car_make]:
        # print(car_make + ' ' + car_model) #test bit
        car_url = craigslist_short + car_make + '+' + car_model + '&min_auto_year=' + min_year + '&max_auto_year=' + max_year
        car_res = requests.get(car_url)
        car_res.raise_for_status()
        soup = BeautifulSoup(car_res.text, 'html.parser')
        car_select = soup.select('div .rows')[0].find_all('span', class_ = 'result-price')

        total = 0
        car_count = 0

        for i in car_select:
            total += int(str(i.string).replace('$', ''))
            car_count += 1
        
        car_data.setdefault(car_make + ' ' + car_model, []).append(str(total/car_count))

        fuel_url = fuel_short + min_year + '&year2=' + max_year + '&make=' + car_make + '&baseModel=' + car_model + '&srchtyp=ymm'

        fuel_res = requests.get(fuel_url)
        fuel_res.raise_for_status()
        fuel_soup = BeautifulSoup(fuel_res.text, 'html.parser')
        fuel_select = fuel_soup.select('div .panel-body')[0].find('td', class_ = 'mpg-comb')

        car_data.setdefault(car_make + ' ' + car_model, []).append(str(fuel_select.string))

        sleep(1)



print(car_data['honda accord'])

# DICTIONARY TEST
for i in car_data:
    for j in car_data[i]:
        print(i + ' ' + j)








# print(url)



# print(select) # print found car prices
# print(type(select))  #used to figure out types of different outputs

# below loop prints out car prices as strings

# for i in select:
#     print(i.string)
