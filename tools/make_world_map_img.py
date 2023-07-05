"""Make the map image"""
import os
from time import sleep
from PIL import Image
import requests

ZOOM = 7

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

def join_tiled_images(image_paths, x_tiles, y_tiles, output_path):
    """Function to join map tiles together into one image"""
    # Open the first tile to get the size
    first_tile = Image.open(image_paths[0])
    tile_width, tile_height = first_tile.size

    # Calculate the total size of the joined image
    joined_width = tile_width * x_tiles
    joined_height = tile_height * y_tiles

    # Create a new blank image for the joined image
    joined_image = Image.new('RGB', (joined_width, joined_height))

    # Iterate over the tiles and paste them into the joined image
    x_count = 0
    y_count = 0
    for tile_path in image_paths:
        tile = Image.open(tile_path)
        joined_image.paste(tile, (y_count * tile_height, x_count * tile_width))
        x_count += 1
        if x_count >= x_tiles:
            x_count = 0
            y_count += 1

    # Save the joined image
    joined_image.save(output_path)

# Download Tiles
print("Downloading Tiles")
image_array = []
for x in range(X_TILES):
    for y in range(Y_TILES):
        print("Downloading:", x, y)
        r_image = requests.get(f"http://tile.openstreetmap.org/{ZOOM}/{x}/{y}.png",
                               timeout=20, headers=HEADERS)
        if not os.path.exists(f"/tmp/map-tiles/{x}"):
            os.makedirs(f"/tmp/map-tiles/{x}")
        with open(f"/tmp/map-tiles/{x}/{y}.png", "wb") as image:
            image.write(r_image.content)
            image_array.append(f"/tmp/map-tiles/{x}/{y}.png")
        sleep(0.01)

# Make Map
print("Making image array")
join_tiled_images(image_array, X_TILES, Y_TILES, "sdcard/ADSB/world_map.png")
