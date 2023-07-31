import pandas
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="geo")

COUNTRY_NAMES = {
    'DE': 'Germany',
    'US': 'United States',
    'CN': 'China'
}

def geo_locate(iso_code, location):
    if location == '':
        return ''

    result = geolocator.geocode(COUNTRY_NAMES[iso_code] + ', ' + location)

    if result == None:
        print(location, ' not found.')
        return None

    print('Found ', location, ' - Address ', result.address, 'lat: ', result.latitude, 'long: ', result.longitude)

    time.sleep(1)

    return result

location_cache = {}

source = pandas.read_csv('../data/COYPU_geo.csv')
source['city'] = source['city'].fillna('')

target = open('./coypu_geolocate.csv', mode='a', encoding='utf-8')

for index, row in source.iterrows():

    if index % 100 == 0:
        print('Reached index ', index)

    if row['city'] == '':
        print('Skip empty location index ', row['company'])
        target.write(row['company'] + ',' + ',' + ',' + '\n')

        continue

    location_key = row['Country'] + ', ' + row['city']

    if location_key in location_cache != None:
        print('Found ' + location_key + ' in cache')
        result = location_cache[location_key]
    else:
        try:
            result = geo_locate(row['Country'], row['city'])
            location_cache[location_key] = result
        except:
            print('Request timed out. Location is ', location_key, 'On data index ', row['company'], '. Skipping the failed location.')
            target.write(row['company'] + ',' + ',' + ',' + '\n')
    
            time.sleep(1)
            continue

    if result != None:
        target.write(row['company'] + ',"' + row['city'].replace('"', '\'') + '","' + result.address.replace('"', '\'') +
                    '",' + str(result.latitude) + ',' + str(result.longitude) + '\n')
    else:
        target.write(row['company'] + ',"' + row['city'].replace('"', '\'') + '",' + ',' + '\n')

target.close()
