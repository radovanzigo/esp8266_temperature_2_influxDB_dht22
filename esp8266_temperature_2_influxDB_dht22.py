sleep_wifi_init=5
sleep_main_cycle=10

import network
import time

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect("Wifi", "passwd")
    time.sleep(sleep_wifi_init) # waiting for wifi
    while not sta_if.isconnected():
        pass
print(sta_if.ifconfig())



import dht
import machine
led = machine.Pin(16, machine.Pin.OUT)
try:
    d = dht.DHT22(machine.Pin(4))
except:
    print ("Initial sensor timeout, continuing..") 

import urequests
import ubinascii

user_and_pass = str(ubinascii.b2a_base64("%s:%s" % ("DB_User", "DB_Passwd"))[:-1], 'utf-8')
headers = {'Authorization': 'Basic %s' % user_and_pass}
print (headers)

while True:
    try:
      led.value(0)  # led on
      d.measure()
      esp8266_temp = d.temperature()
      esp8266_hum = d.humidity()
    except:
      print("Sensor timeout, retrying..")
      time.sleep(sleep_main_cycle)
      continue

    url_string = 'https://domanin.com/write?db=opentsdb'
    data_string = 'metric=esp8266_temp,host=sensor1 value=%s' % (esp8266_temp)
    data_string = '%s\nmetric=esp8266_hum,host=sensor1 value=%s' % (data_string, esp8266_hum)
    print(data_string)
    try:
      r = urequests.post(url_string, data=data_string, headers=headers)
      r.close()
    except:
      print("Unable to submit data to server")
    led.value(1)  # led off
    time.sleep(sleep_main_cycle)

  
