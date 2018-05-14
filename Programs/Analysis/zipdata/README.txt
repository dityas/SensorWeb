The data is in form of csv files named according to the metric.

All the csvs contain data for all 12 BBBs stacked as columns since the BBBs were time synced. 
To select data for a particular 'n' node, all columns containing string 'bb{n}localdomian' should be selected.

All the data is not used since some of it is corrupted due to networking problems in BBBs.

From all csvs, the data for bb1,bb2,bb3,bb4 is used as training data. 
From all csvs, the data for bb5 is used as testing data.

All other data is corrupted. Since the BBBs got disconnected by themselves.

If all data is aggregated per BBB, there should be 29 columns as follows

0: cpu_value host bb{n}localdomain type_instance idle
1: cpu_value host bb{n}localdomain type_instance interrupt
2: cpu_value host bb{n}localdomain type_instance nice
3: cpu_value host bb{n}localdomain type_instance softirq
4: cpu_value host bb{n}localdomain type_instance steal
5: cpu_value host bb{n}localdomain type_instance system
6: cpu_value host bb{n}localdomain type_instance user
7: cpu_value host bb{n}localdomain type_instance wait
8: interface_tx host bb{n}localdomain instance lo type if_dropped
9: interface_tx host bb{n}localdomain instance lo type if_errors
10: interface_tx host bb{n}localdomain instance lo type if_octets
11: interface_tx host bb{n}localdomain instance lo type if_packets
12: interface_tx host bb{n}localdomain instance wlan0 type if_dropped
13: interface_tx host bb{n}localdomain instance wlan0 type if_errors
14: interface_tx host bb{n}localdomain instance wlan0 type if_octets
15: interface_tx host bb{n}localdomain instance wlan0 type if_packets
16: interface_rx host bb{n}localdomain instance lo type if_dropped
17: interface_rx host bb{n}localdomain instance lo type if_errors
18: interface_rx host bb{n}localdomain instance lo type if_octets
19: interface_rx host bb{n}localdomain instance lo type if_packets
20: interface_rx host bb{n}localdomain instance wlan0 type if_dropped
21: interface_rx host bb{n}localdomain instance wlan0 type if_errors
22: interface_rx host bb{n}localdomain instance wlan0 type if_octets
23: interface_rx host bb{n}localdomain instance wlan0 type if_packets
24: contextswitch_value host bb{n}localdomain type contextswitch
25: disk_io_time host bb{n}localdomain instance mmcblk1 type disk_io_time
26: disk_io_time host bb{n}localdomain instance mmcblk1boot0 type disk_io_time
27: disk_io_time host bb{n}localdomain instance mmcblk1boot1 type disk_io_time
28: disk_io_time host bb{n}localdomain instance mmcblk1p1 type disk_io_time


Training set:

There is a transient anomaly at data point 1745 (Time: 2018-03-13 06:25:35+00:00) and lasts for around 100 data points. 
This can be ignored i.e. manually flattened or if the algorithm is robust, you can just include it.


Test set:

Application changes on test node at point 42830 (Time: 2018-03-15 15:34:10+00:00).
