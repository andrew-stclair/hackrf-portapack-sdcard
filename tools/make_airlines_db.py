"""Requests module to download the """
import unicodedata
import requests

print("Downloading DB TXT")
csv_file = requests.get(
    "https://raw.githubusercontent.com/kx1t/planefence-airlinecodes/main/airlinecodes.txt",
    timeout=20
).text

print("Generating airlines.db")
print(f"| {'code':<4} | {'airline':<32} | {'country':<32} |")
print("|:----:|:--------------------------------:|:--------------------------------:|")
icao_codes=bytearray()
airlines_countries=bytearray()
ROW_COUNT=0
with open("sdcard/ADSB/airlines.db", "wb") as database:
    csv_file = csv_file.split('\n')
    for row in csv_file[1:]:
        row = row.split(',')
        icao_code=row[0]
        if not row == ['']:
            # Normalize some unicode characters
            airline=unicodedata.normalize('NFKD', row[1][:32]).encode('ascii', 'ignore')
            country=unicodedata.normalize('NFKD', row[3][:32]).encode('ascii', 'ignore')
            print(f"| {row[0]:<4} | {airline.decode():<32} | {country.decode():<32} |")
            if len(icao_code) == 3 :
                airline_padding=bytearray()
                country_padding=bytearray()
                icao_codes=icao_codes+bytearray(icao_code+'\0', encoding='ascii')
                airline_padding=bytearray('\0' * (32 - len(airline)), encoding='ascii')
                country_padding=bytearray('\0' * (32 - len(country)), encoding='ascii')
                airlines_countries=airlines_countries+bytearray(
                    airline+airline_padding+country+country_padding
                )
                ROW_COUNT+=1
print("done")
