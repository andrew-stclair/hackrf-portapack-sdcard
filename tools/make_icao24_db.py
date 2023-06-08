"""Import Modules"""
import csv
import requests

icao24_codes=bytearray()
data=bytearray()
ROW_COUNT=0

with open("sdcard/ADSB/icao24.db", "wb") as database:
    print("Downloading icao24 DB CSV")
    csv_file = requests.get("https://opensky-network.org/datasets/metadata/aircraftDatabase.csv",
    timeout=20).text.split('\n')
    print("Generating icao24.db")
    for row in csv.reader(sorted(csv_file[1:]), skipinitialspace=True):
        # only store in case enough info is available
        if len(row) == 27 and len(row[0]) == 6 and len(row[1]) > 0:
            print(row)
            icao24_code=row[0][:6].upper()
            registration=row[1][:8].encode('ascii', 'ignore')
            manufacturer=row[3][:32].encode('ascii', 'ignore')
            model=row[4][:32].encode('ascii', 'ignore')
            # in case icao aircraft type isn't, use ac type like BALL for balloon
            if len(row[8]) == 3:
                actype=row[8][:3].encode('ascii', 'ignore')
            else:
                actype=row[5][:4].encode('ascii', 'ignore')
            owner=row[13][:32].encode('ascii', 'ignore')
            operator=row[9][:32].encode('ascii', 'ignore')
            #padding
            icao24_codes.extend(bytearray(icao24_code+'\0', encoding='ascii'))
            registration_padding=bytearray('\0' * (9 - len(registration)), encoding='ascii')
            manufacturer_padding=bytearray('\0' * (33 - len(manufacturer)), encoding='ascii')
            model_padding=bytearray('\0' * (33 - len(model)), encoding='ascii')
            actype_padding=bytearray('\0' * (5 - len(actype)), encoding='ascii')
            owner_padding=bytearray('\0' * (33 - len(owner)), encoding='ascii')
            operator_padding=bytearray('\0' * (33 - len(operator)), encoding='ascii')
            data.extend(bytearray(
                registration
                +registration_padding
                +manufacturer
                +manufacturer_padding
                +model
                +model_padding
                +actype
                +actype_padding
                +owner
                +owner_padding
                +operator
                +operator_padding
            ))
            ROW_COUNT+=1
    database.write(icao24_codes+data)
print("Total of", ROW_COUNT, "ICAO codes stored in database")
