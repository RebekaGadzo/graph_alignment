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

source = pandas.read_csv('SCM_geo.csv')
source['Location'] = source['Location'].fillna('')

target = open('./SCM_geolocate.csv', mode='a', encoding='utf-8')

for index, row in source.iterrows():
    if row['index'] % 100 == 0:
        print('Reached index ', row['index'])

    if row['Location'] == '':
        print('Skip empty location index ', row['index'])
        target.write(str(row['index']) + ',' + ',' + ',' + '\n')

        continue

    location_key = row['Country'] + ', ' + row['Location']

    if location_key in location_cache != None:
        print('Found ' + location_key + 'in cache')
        result = location_cache[location_key]
    else:
        while True:
            try:
                result = geo_locate(row['Country'], row['Location'])
                location_cache[location_key] = result
                break
            except:
                print('Request timed out. Location is ', location_key, 'On data index ', row['index'])
                print('Retrying request in 300 seconds')
                time.sleep(300)
                print('Retrying request')

                continue

    if result != None:
        target.write(str(row['index']) + ',"' + row['Location'].replace('"', '\'') + '","' + result.address.replace('"', '\'') +
                    '",' + str(result.latitude) + ',' + str(result.longitude) + '\n')
    else:
        target.write(str(row['index']) + ',"' + row['Location'].replace('"', '\'') + '",' + ',' + '\n')

target.close()
