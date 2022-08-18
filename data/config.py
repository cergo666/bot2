import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

user_agent = '"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"'
url = 'https://ryazan.camera'
kreml_id = '2949083/7859f90e1443792efa8f'
post_id = '3135021/24154bef12404d570d9d'
narodmon_url = 'https://narodmon.ru/api/sensorsOnDevice?id=6679&uuid=f0d6111ac3e7887141dd21b22a52e73a&api_key=2EAZSHH1PYKdf&lang=en'
rain_url = 'https://yandex.ru/pogoda/maps/nowcast?le_Lightning=1&lat=54.65699340751401&lon=39.66930123754882&ll=39.773543_54.617214&z=8'
pogoda_url = 'https://yandex.ru/pogoda/?lat=54.65699340751401&lon=39.66930123754882'
gismeteo10_url = 'https://www.gismeteo.ru/weather-ryazan-4394/10-days/'
traffic_url = 'https://yandex.ru/maps/11/ryazan/?l=trf%2Ctrfe&ll=39.738739%2C54.631886&z=13.4'
fires_url = 'http://www.aerocosmos.info/emergency_search/'
if os.name == 'nt':
    ffmpeg = 'bin/ffmpeg.exe'
    binary = 'firefox_binary=bin/geckodriver.exe'
else:
    ffmpeg = 'ffmpeg'
    binary = ''
def driver_init():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(binary, options=options)
    return driver
