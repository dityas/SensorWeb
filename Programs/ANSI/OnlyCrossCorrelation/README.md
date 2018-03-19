
Made by: Maria and Sili

Date: 06/22/2017

/***********PROGRAM DOCUMENTATION*********************/

Each CORE virtual node reads an specific sweetwater database. Then the following steps are performed:

1. Each node pre-processes 5 minutes of sweetwater data each round. The pre-processing includes: (i) remove instrument noise; (ii) taping process, (iii) whitenning process.

2. Each node compress the data using zlib and send it via UDP to its neighbors. 


/***********REQUIREMENTS******************************/

1. Use CORE emulator for running the program.

2. The program requires you install zlib library. To install zlib, you must do the following:

wget http://www.zlib.net/zlib-1.2.11.tar.gz (Please check current version here: http://www.zlib.net/)
tar -xvzf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=/usr/local/zlib
make
sudo make install


3. You should install the following library for using mysql

sudo apt-get install  libmysqlcppconn-dev


/************STEPS************************************/

1. Copy the folder in your .core folder
   e.g.  /home/user/.core/ValveCore

2. Open db.sh

3. Change the path to your computer user
   HOME="/home/USER/.core"
   homefolder='/home/USER/.core/ValveCore'

3. Set up your /home/USER/.core/myservices/sample.py to the new path
   _startup = ('sh /home/USER/.core/ValveCore/db.sh',)

4. Create a mesh network in CORE (or use imn map in the folder imn)

5. Set IP wireless network to 172.16.0.0/24

6. Link all routers to the wireless network

7. Run the program (Because this is an example, you may change the database and the time to recover data in db.sh, in other words, change the parameters to the program)

./read $nodeid 172.16.0.254 oasis nodeConfiguration.dat 20140321000000 420 >> log.out

8. Open log.out to see log file




