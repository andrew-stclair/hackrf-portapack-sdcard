"""Import Modules"""
import os
import pyvips
import requests

ZOOM = 6

# Headers for request
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Host": "tile.openstreetmap.org",
    "User-Agent": "Requests Python3.11",
    "Accept-Language": "en-AU,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# Calculate number of tiles
X_TILES = int(2**ZOOM)
Y_TILES = int(2**ZOOM)
print("Tiles:", X_TILES, Y_TILES)

# Calculate final map size in pixels
X_PIXELS = X_TILES*256
Y_PIXELS = Y_TILES*256
print("Pixels:", X_PIXELS, Y_PIXELS)

# Download Tiles
print("Downloading Tiles")
for x in range(X_TILES):
    for y in range(Y_TILES):
        print("Downloading:", x, y)
        r_image = requests.get(f"http://tile.openstreetmap.org/{ZOOM}/{x}/{y}.png",
                               timeout=20, headers=HEADERS)
        if not os.path.exists(f"/tmp/map-tiles/{x}"):
            os.makedirs(f"/tmp/map-tiles/{x}")
        with open(f"/tmp/map-tiles/{x}/{y}.png", "wb") as image:
            image.write(r_image.content)

# Make Map
print("Making image array")
tiles = [pyvips.Image.new_from_file(f"/tmp/map-tiles/{x}/{y}.png", access="sequential")
         for x in range(X_TILES) for y in range(Y_TILES)]
print("Joining array into single image")
image = pyvips.Image.arrayjoin(tiles, across=X_TILES)
print("Saving image")
image.write_to_file("sdcard/ADSB/world_map.jpg")
