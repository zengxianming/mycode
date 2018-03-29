# Generates the csv file everything else is built from.
# Basically a poor man's cache for the Supercharger data.
# reference ： https://github.com/sdroadie/supercharger-distance
import time
from geopy.geocoders import GoogleV3
import re
import pandas as pd

geocoder = GoogleV3(api_key='AIzaSyDyCKnMY2J28RDYIpURCrjTjeFpx5ugMvs')
df = pd.read_excel("C:\\Users\\D\\Desktop\\superchargers1.xlsx")
Address = df[(df.lat.isnull()) & (df.address.notnull())].address.tolist()
superchargers = []

for full_address in Address:
    location = geocoder.geocode(full_address, timeout=10)
    print(full_address)
    time.sleep(1.5)  # so we don't overrun the per-second limit of the Google API.
    address = full_address
    locality = df[df.address == full_address].iloc[0, 1]
    location_map = {'address': re.escape(address),
                    'locality': re.escape(locality)}
    try:
        location_map['lat'] = str(location.latitude)
        location_map['long'] = str(location.longitude)
    except AttributeError:
        print('Could not find coordinates for {}'.format(full_address))
    finally:
        if 'lat' not in location_map:
            location_map['lat'] = ''
        if 'long' not in location_map:
            location_map['long'] = ''
        superchargers.append(location_map)

with open('C:\\Users\\D\\Desktop\\add_superchargers.csv', 'w') as csv_file:
    # Write legend row.
    csv_file.write('address,locality,lat,long\n')
    for s in superchargers:
        csv_file.write(','.join([
            s['address'],
            s['locality'],
            s['lat'],
            s['long']]) + '\n')
