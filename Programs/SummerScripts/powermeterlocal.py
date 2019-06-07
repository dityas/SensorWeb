from ina219 import INA219, DeviceRangeError
from time import sleep
import subprocess
import sys

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

def read_ina219():
    # http_post = "curl -i -XPOST \'http://172.22.114.74:8086/write?db=em_collectd\' -u aditya:123 --data-binary \'"
    try:
        # print('Bus Voltage: {0:0.2f}V'.format(ina.voltage()))
        voltage = ina.voltage()
        # print('Bus Current: {0:0.2f}mA'.format(ina.current()))
        current = ina.current()
        # print('Power: {0:0.2f}mW'.format(ina.power()))
        power = ina.power()
        # print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
        shunt_voltage = ina.shunt_voltage()
        http_post = "curl -i -XPOST \'http://192.168.1.2:8086/write?db=collectd\' -u admin:admin --data-binary \'"
        http_post += "\nBus_Voltage8,type=Bus_Voltage8 value=" 
        http_post += str(voltage)
        http_post += "\n"
        http_post += "\nBus_Current8,type=Bus_Current8 value=" 
        http_post += str(current)
        http_post += "\n"
        http_post += "\nPower8,type=Power8 value=" 
        http_post += str(power)
        http_post += "\n"
        http_post += "\nShunt_Voltage8,type=Shunt_Voltage8 value=" 
        http_post += str(shunt_voltage)
        http_post += "\'"
        # print http_post
        subprocess.call(http_post, shell=True)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)

while 1:
    read_ina219()
    sleep(2)
