import requests
import os

from bs4 import BeautifulSoup
from time import sleep

# sample_url = 'https://losangeles.craigslist.org/search/cto?auto_make_model=honda+accord&min_auto_year=2016&max_auto_year=2019'
# fuel_economy = 'https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1=2016&year2=2016&make=Volkswagen&baseModel=Passat&srchtyp=ymm'

print('MONTHLY COSTS OF ALTERNATIVE TRANSPORTATION METHODS')
print()

def rideshare_busses():
    #Calculation of public transportation costs for me

    bus_fare = 1.75
    uber_weekends = 12.44   #average cost of a trip I take on weekends
    uber_weekdays = 8.12    #average cost of a trip I use to commute to ucla x

    #alternative 1 - Using busses only for weekdays and uber on weekends
    per_month_1 = (uber_weekends * 16) + (bus_fare * 24)
    print('alternative 1 - Using busses only for weekdays and uber on weekends')
    print('Cost : $' + str(round(per_month_1,2)))

    #alternative 2 - Using uber one way in weekdays
    per_month_2 = (uber_weekends * 16) + (uber_weekdays * 12) + (bus_fare *12)
    print('alternative 2 - Using uber one way in weekdays and uber on weekends')
    print('Cost : $' + str(round(per_month_2,2)))

    #alternative 3 - Using uber only
    per_month_3 = (uber_weekends * 16) + (uber_weekdays * 24)
    print('alternative 3 - Using uber only')
    print('Cost : $' + str(round(per_month_3,2)))

rideshare_busses()
print()

#Getting data on costs of car ownership costs for me

craigslist_short = 'https://losangeles.craigslist.org/search/cto?auto_make_model='
fuel_short = 'https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1='

#cars to look up
cars = {'honda' : ['accord', 'civic'], \
    'audi' : ['a3', 'a4'], \
    'ford' : ['focus'], \
    'lexus' : ['es+350'], \
    'chevrolet' : ['silverado'], \
    'bmw' : ['328i', '528i'], \
    'volkswagen' : ['passat', 'jetta'], \
    'kia' : ['sorento', 'optima'], \
    'hyundai' : ['sonata'], \
    'toyota' : ['prius', 'corolla']}

min_year = '2016'
max_year = '2016'

car_data = {} # this is the main dictionary to keep information in

#get car prices from craigslist and fuel economy mpg from fueleconomy.gov
for car_make in cars:
    for car_model in cars[car_make]:
        try:
            car_url = craigslist_short + car_make + '+' + car_model + '&min_auto_year=' + min_year + '&max_auto_year=' + max_year
            car_res = requests.get(car_url)
            car_res.raise_for_status()
            soup = BeautifulSoup(car_res.text, 'html.parser')
            car_select = soup.select('div .rows')[0].find_all('span', class_ = 'result-price')

            total = 0
            car_count = 0

            for i in car_select: #i here is the item price for a single car
                car_price = int(str(i.string).replace('$',''))
                if(car_price >= 4000 & car_price <=45000):
                    total += car_price
                    car_count += 1
            
            car_data.setdefault(car_make + ' ' + car_model, []).append(str(total/car_count))

            fuel_url = fuel_short + min_year + '&year2=' + max_year + '&make=' + car_make + '&baseModel=' + car_model + '&srchtyp=ymm'

            fuel_res = requests.get(fuel_url)
            fuel_res.raise_for_status()
            fuel_soup = BeautifulSoup(fuel_res.text, 'html.parser')
            fuel_select = fuel_soup.select('div .panel-body')[0].find('td', class_ = 'mpg-comb')

            car_data.setdefault(car_make + ' ' + car_model, []).append(str(fuel_select.string))

            sleep(0.1)
        except:
            print('Car data not found for: ' + car_make + ' ' + car_model)


#costs of different cars monthly for me per month

# assumptions : # I will own the car for a year
                # It will be around a few years of age 
                # I can expect 10% value depreciation
#static prices for all cars
insurance_cost = 849 #average in california
avg_parking_weekdays = 5
avg_parking_weekends = 8
monthly_parking_fees = (avg_parking_weekdays * 12) + (avg_parking_weekends * 8)
avg_car_maintenance_monthly = 57 #average in california

monthly_static = avg_car_maintenance_monthly + monthly_parking_fees + (insurance_cost / 12)


#gas comsumption calculations
gas_price_average = 3.51
avg_trip_miles_weekends = 9.2
avg_trip_miles_weekdays = 5.2
monthly_trip_length = (avg_trip_miles_weekends * 16) + (avg_trip_miles_weekdays * 24)

per_month_cars = {}

for car in car_data:
    try:
        if car_data[car][1] != 0:
            monthly_gas_cost_per_car = (monthly_trip_length / int(car_data[car][1])) * gas_price_average
            car_physical_cost = float(car_data[car][0]) / 120
            calculated_avg = monthly_gas_cost_per_car + monthly_static + car_physical_cost
            per_month_cars.setdefault(car, '$' + str(round(calculated_avg, 2)))
    except:
        pass
print()
print('Costs of different cars per month: ')
print()

try:
    for key,value in per_month_cars.items():
        print(key + ' costs ' + value)
except:
    print('Not printing ' + key)
