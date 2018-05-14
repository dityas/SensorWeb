#!/bin/bash

HOME="/home/maria/.core"
homefolder='/home/maria/.core/ValveCore'
savefolder='/home/maria/.core/ValveCore/TestResults/R1'
nodeid=`echo "$(pwd)" | grep -Eo "[[:digit:]]+" | tail -n1`

ifconfig eth0 broadcast 172.16.255.255 
/usr/lib/quagga/zebra -u root -g root
/usr/lib/quagga/batmand eth0
ip rule add from all lookup 66
subfolder=$nodeid
sleep 15

#mkdir $subfolder
#cp $homefolder/data/$subfolder/data.dat $subfolder
cp $homefolder/nodeConfiguration.dat nodeConfiguration.dat
cp $homefolder/javaReader.jar javaReader.jar

sudo g++ -Wall -g -pthread -std=c++11 -o read $homefolder/coresql.cpp $homefolder/csql.cpp $homefolder/valveSql.cpp $homefolder/communication.cpp $homefolder/PracticalSocket.cpp -I/usr/include/cppconn  -L/usr/lib -lmysqlcppconn -lz
#sudo g++ -Wall -std=c++11 -o read $homefolder/coresql.cpp $homefolder/csql.cpp $homefolder/valveSql.cpp $homefolder/PracticalSocket.cpp -I/usr/include/cppconn  -L/usr/lib -lmysqlcppconn

mkdir cross
./read $nodeid 172.16.0.254 oasis nodeConfiguration.dat 20140321000100 120 >> log.out

mkdir DONE
cp -r cross $savefolder/$nodeid


#g++ -Wall -g -std=c++11 -o communication -pthread $homefolder/communication.cpp $homefolder/PracticalSocket.cpp

#sleep 1
#./communication >> log.out



