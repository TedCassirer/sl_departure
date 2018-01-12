from RPLCD.gpio import CharLCD
from RPi import GPIO
import time
import re
from collections import defaultdict
from departures import *


def clean_string(string):
    string = "".join(map(lambda c: special_chars.get(c, c), string))

    # Removes anything within () or []
    string = re.sub("[\(\[].*?[\)\]]", "", string)
    return string

# GPIO.setwarnings(False)

lcd = CharLCD(cols=20, rows=4, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)

special_chars = defaultdict(lambda x: None)
special_chars["å"] = chr(0)
special_chars["ä"] = chr(1)
special_chars["ö"] = chr(2)

special_chars_code = [(
    0b00100,
    0b01010,
    0b00100,
    0b01010,
    0b10001,
    0b11111,
    0b10001,
    0b00000
    ),
    (0b00000,
     0b01010,
     0b00000,
     0b01010,
     0b10001,
     0b11111,
     0b10001,
     0b00000
    ),
    (0b00000,
     0b01010,
     0b00000,
     0b01110,
     0b10001,
     0b10001,
     0b01110,
     0b00000
    ),

]
for i, spc in enumerate(special_chars_code):
    lcd.create_char(i, spc)

lcd.write_string("Testing")
lcd.clear()

trips = [("Vårdcentralen (Värmdö)", "Slussen"), ("Farstaviken", "Slussen")]

while True:
    rows = []
    for t in trips:
        try:
            departures = get_departures(t[0], t[1])
            origin_name = departures[0]["LegList"]["Leg"][0]["Origin"]["name"] + ":"
            departure_times = ", ".join(map(lambda d: d["LegList"]["Leg"][0]["Origin"]["time"][:-3], departures[:3]))
        except Exception as e:
            print(e)
            r1 = clean_string(t[0]) + ":"
            r2 = "No bus silly woman"
            lcd.write_string(r1[:20])
            lcd.write_string("\n\r")
            lcd.write_string(r2[:20])
            lcd.write_string("\n\r")
            print(r1)
            print(r2)
            continue
        rows.append(origin_name)
        rows.append(departure_times)
        for r in rows:
            r = clean_string(r)
            print(r)
            lcd.write_string(r[:20])
            lcd.write_string("\n\r")
        print("\n---\n")
    time.sleep(600)
    lcd.clear()

