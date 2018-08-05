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

	# Read CPU
	user, system, iowait = read_cpu()

	# Read net
	wlan0_TX, wlan0_RX = read_net()

	# Read disk
	p1, p2 = read_disk()

        shunt_voltage = ina.shunt_voltage()
        http_post = "curl -i -XPOST \'http://http://172.22.114.74:8086/write?db=em_collectd_power\' -u admin:admin --data-binary \'"
        http_post += "\nBus_Voltage10,type=Bus_Voltage10 value=" 
        http_post += str(voltage)
        http_post += "\n"
        http_post += "\nBus_Current10,type=Bus_Current10 value=" 
        http_post += str(current)
        http_post += "\n"
	http_post += "\nCPU_user,type=CPU_user value=" 
	http_post += str(user)
	http_post += "\n"
	http_post += "\nCPU_system,type=CPU_system value=" 
	http_post += str(system)
	http_post += "\n"
	http_post += "\nnet_TX,type=net_TX value=" 
	http_post += str(wlan0_TX)
	http_post += "\n"
	http_post += "\nnet_RX,type=net_RX value=" 
	http_post += str(wlan0_RX)
	http_post += "\n"
	http_post += "\ndisk_p1,type=disk_p1 value=" 
	http_post += str(p1)
	http_post += "\n"
	http_post += "\ndisk_p2,type=disk_p2 value=" 
	http_post += str(p2)
	http_post += "\n"
        http_post += "\nPower10,type=Power10 value=" 
        http_post += str(power)
        http_post += "\n"
        http_post += "\nShunt_Voltage10,type=Shunt_Voltage10 value=" 
        http_post += str(shunt_voltage)
        http_post += "\'"
        # print http_post
        subprocess.call(http_post, shell=True)
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)

def read_cpu():
    data = open("/proc/stat","r").readlines()[0]
    data = data.split()
    user = data[1]
    system = data[3]
    iowait = data[5]
    return (user, system, iowait)

def read_net():
    data = open("/proc/net/dev","r").readlines()[2]
    data = data.split()
    wlan0_RX = data[2]
    wlan0_TX = data[10]
    return (wlan0_TX, wlan0_RX)

def read_disk():
    data = open("/proc/diskstats","r").readlines()
    p1 = data[-2].split()[-1]
    p2 = data[-1].split()[-1]
    return (p1, p2)

while 1:
    read_ina219()
    sleep(2)
