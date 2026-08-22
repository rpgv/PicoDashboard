from machine import Pin
import network
import time
import requests
import utime
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Define wifi connection 
ssid = ''
password = ''

# Define led for debugging
led = Pin("LED", Pin.OUT)

# Define screen to display information
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)   

# Define buttons with internal pull-ups
btn_1 = Pin(2, Pin.IN, Pin.PULL_UP) 
btn_2 = Pin(3, Pin.IN, Pin.PULL_UP) 

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connection
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)

    print('Connected!')
    print('Network config (IP, Mask, Gateway, DNS):', wlan.ifconfig())

    lcd.putstr("Connected to Wi-fi")
    utime.sleep(2)
    lcd.clear()
    blink()
        

def blink():
    for _ in range(3):
        led.value(1)
        time.sleep(1)
        led.value(0)
        time.sleep(1)
    led.value(1)

def request_and_display(option):
    print("BTN 02")
    print("Making request ...")
    response = requests.get(f'http://192.168.1.252:8000/{option}')
    print(f"Made request to {str(response.content)}")
    lcd.putstr(f"{response.content}")
    utime.sleep(5)
    lcd.clear() 

### Initiating constants for requests
# Defines intial state request to 'page 0'
option = 0

option_map = {
    0 : 'Home page',
    1 : 'Weather',
    2 : 'Population',
}

# Defines iterative counter on request so that it doesn't overwhelms the API
request_timer = 0

# Booting up cycle
print("Connecting to WIFI...")
connect_wifi()

while True:
    # Cycle through options
    if btn_1.value() == 0:  # button pressed (LOW)
        led.value(1)
        print('--')
        print("BTN 01")
        print("Selecting options")
        request_timer = 0
        option+=1
        if option > 2:
            option = 0
        print(f"Selected option {option}")
        lcd.putstr(f"Selected option: {option_map[option]}")
        utime.sleep(2)
        lcd.clear()
        
    else:
        led.value(0)
    # Make request to update screen information or to select another option
    if btn_2.value() == 0:  # button pressed (LOW)
        led.value(1)
        request_timer = 0
        request_and_display(option)
    else:
        led.value(0)

    # Iteratively make requests roughly every minute 
    request_timer += 1
    if request_timer == 120:
        request_and_display(option)
        request_timer = 0 # Reset request timer



    time.sleep(0.3)  # small delay for button debounce
