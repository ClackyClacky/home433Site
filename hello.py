#!/usr/bin/env python3

from flask import Flask, render_template, request
from rpi_rf import RFDevice
from flask_bootstrap import Bootstrap, WebCDN
from apscheduler.schedulers.background import BackgroundScheduler
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz
import logging
import sys
utc = pytz.UTC
app = Flask(__name__)
Bootstrap(app)

scheduler = BackgroundScheduler()

city = LocationInfo("Limerick", "Ireland", "Europe/London", 52.712380, -8.608660)
sun_stats = sun(city.observer, date=datetime.datetime.today())
sunset_time = sun_stats['sunset']


PC_LAMP_ON_CODE = 4117
PC_LAMP_OFF_CODE = 4116
TV_LEFT_ON_CODE = 421
TV_LEFT_OFF_CODE = 420
TV_RIGHT_ON_CODE = 21
TV_RIGHT_OFF_CODE = 20

rfdevice = RFDevice(17)
rfdevice.enable_tx()
rfdevice.tx_repeat = 10

pc_lamp_status = False

def counter(pc_lamp_status):
    city = LocationInfo("Limerick", "Ireland", "Europe/London", X, Y)
    sun_stats = sun(city.observer, date=datetime.datetime.today())
    sunset_time = sun_stats['sunset']
    time = utc.localize(datetime.datetime.now())
    if pc_lamp_status:
        if time > sunset_time and not pc_lamp_status:
            rfdevice.tx_code(PC_LAMP_ON_CODE, None, None, None)
            pc_lamp_status = True
    else:
        rfdevice.tx_code(PC_LAMP_OFF_CODE, None, None, None)
        pc_lamp_status = False
        return None


job = scheduler.add_job(counter, 'interval', minutes=5, args=[pc_lamp_status])
scheduler.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pc_lamp', methods=['GET', 'POST'])
def switch_pc_lamp():

    if "PC_ON" in request.form:
        rfdevice.tx_code(PC_LAMP_ON_CODE, None, None, None)
    if "PC_OFF" in request.form:
        rfdevice.tx_code(PC_LAMP_OFF_CODE, None, None, None)
    if "TV_LEFT_ON" in request.form:
        rfdevice.tx_code(TV_LEFT_ON_CODE, None, None, None)
    if "TV_LEFT_OFF" in request.form:
        rfdevice.tx_code(TV_LEFT_OFF_CODE, None, None, None)
    if "TV_RIGHT_ON" in request.form:
        rfdevice.tx_code(TV_RIGHT_ON_CODE, None, None, None)
    if "TV_RIGHT_OFF" in request.form:
        rfdevice.tx_code(TV_RIGHT_OFF_CODE, None, None, None)
    return render_template('index.html', current_time=datetime.datetime.now().strftime("%A, %B %d %Y, %H:%M:%S")
                           , sunset_time=sunset_time.strftime("%A, %B %d %Y, %H:%M:%S"))
