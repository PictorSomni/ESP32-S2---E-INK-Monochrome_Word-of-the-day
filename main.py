#######################################################
#                       IMPORTS                       #
#######################################################
import time
import random
import board
import displayio
import adafruit_ssd1680
from secrets import secrets
import terminalio
from adafruit_display_text import label, wrap_text_to_lines

#### COMMENT FOR WIFI USE
from quotes import positive_quotes
####

##### UNCOMMENT FOR WIFI USE
# import ipaddress
# import ssl
# import wifi
# import socketpool
# import adafruit_requests
#####

#######################################################
#                    SETUP DISPLAY                    #
#######################################################
FOREGROUND_COLOR = 0x000000
BACKGROUND_COLOR = 0xFFFFFF
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 130
# For 8.x.x and 9.x.x. When 8.x.x is discontinued as a stable release, change this.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

displayio.release_displays()

# This pinout works on a Metro M4 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = None  # Set to None for FeatherWing
epd_busy = None  # Set to None for FeatherWing

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000)
time.sleep(1)

# For issues with display not updating top/bottom rows correctly set colstart to 8
display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    busy_pin=epd_busy,
    highlight_color=FOREGROUND_COLOR,
    rotation=270,
)

g = displayio.Group()

#######################################################
#                      SETUP WIFI                     #
#######################################################
##### UNCOMMENT FOR WIFI USE
# URLs to fetch
# JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"

# print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

# print("Available WiFi networks:")
# for network in wifi.radio.start_scanning_networks():
#     print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#                                              network.rssi, network.channel))
# wifi.radio.stop_scanning_networks()

# print(f"Connecting to {secrets['ssid']}")
# wifi.radio.connect(secrets['ssid'], secrets['password'])
# print(f"Connected to {secrets['ssid']}")
# print(f"My IP address: {wifi.radio.ipv4_address}")

# ping_ip = ipaddress.IPv4Address("8.8.8.8")
# ping = wifi.radio.ping(ip=ping_ip)

# # retry once if timed out
# if ping is None:
#     ping = wifi.radio.ping(ip=ping_ip)

# if ping is None:
#     print("Couldn't ping 'google.com' successfully")
# else:
#     # convert s to ms
#     print(f"Pinging 'google.com' took: {ping * 1000} ms")

# pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl.create_default_context())

#######################################################
#                STARTING WEB PARSING                 #
#######################################################
# print(f"Fetching json from {JSON_QUOTES_URL}")
# response = requests.get(JSON_QUOTES_URL)
# parsed_response = response.json()
# text = parsed_response[0]['text']
# author = parsed_response[0]['author']
#####

#######################################################
#                 DICTIONNARY QUOTES                  #
#######################################################
#### COMMENT FOR WIFI USE
quote = random.choice(positive_quotes)
text = quote['quote']
author = quote['author']
print_lines = ""
####

# LIMITS THE TEXT TO 'MAX_LENGTH' CHARACTERS #
MAX_LENGTH = 20
# lines = [text[i:i + MAX_LENGTH] + '\n' for i in range(0, len(text), MAX_LENGTH)]
lines = wrap_text_to_lines(text, MAX_LENGTH)
for line in lines :
    print_lines += f"\n {line}"

print("-" * 40)
print(print_lines)
print(author)
print("-" * 40)


# Set a background
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = BACKGROUND_COLOR
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

# with open("/WHITE.bmp", "rb") as f :
#     pic = displayio.OnDiskBitmap(f)
#     t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
#     g.append(t)

# Draw JSON 'text'
text_group = displayio.Group(scale=2, x=0, y=0)
text_area = label.Label(terminalio.FONT, text=print_lines, color=FOREGROUND_COLOR,line_spacing=1)
text_group.append(text_area)  # Add this text to the text group
g.append(text_group)

# Draw JSON 'author'
text_group = displayio.Group(scale=1, x=120, y=118)
text = author
text_area = label.Label(terminalio.FONT, text=text, color=FOREGROUND_COLOR)
text_group.append(text_area)  # Add this text to the text group
g.append(text_group)

# Place the display group on the screen
display.root_group = g

# Refresh the display to have everything show on the display
# NOTE: Do not refresh eInk displays more often than 180 seconds!
display.refresh()

time.sleep(120)

# Keep the display the same
while True:
    time.sleep(10)
