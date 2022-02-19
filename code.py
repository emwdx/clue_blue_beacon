# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time

from adafruit_clue import clue

from adafruit_ble import BLERadio

from adafruit_ble_eddystone import uid, url

ble = BLERadio()

eddystone_uid = uid.EddystoneUID(ble.address_bytes)
ble.name = "EMW_CLUE"

clue.sea_level_pressure = 1020
UPDATE_INTERVAL = 1.0
SHOW_DISPLAY = True
clue_data = clue.simple_text_display(title="_", title_scale=2)
start_time = time.monotonic()

while True:
    current_time = time.monotonic()
    if(current_time - start_time)>UPDATE_INTERVAL:
        if(SHOW_DISPLAY):
            clue_data[0].text = "Pressure: {:.3f} hPa".format(clue.pressure)
            clue_data[1].text = "Temperature: {:.1f} C".format(clue.temperature)
            clue_data[2].text = "Humidity: {:.1f} %".format(clue.humidity)
            clue_data[3].text = "Light: {:.1f}".format(clue.color[3])
            clue_data[4].text = "Connected: {0}".format(ble.connected)
            clue_data.show()

        sensor_string = "http://,{0},{1},{2}\n".format(round(clue.temperature,1),clue.color[3],round(clue.pressure))

        eddystone_url = url.EddystoneURL(sensor_string)
        ble.start_advertising(eddystone_url)
        time.sleep(1.0)
        ble.stop_advertising()

        start_time = current_time

