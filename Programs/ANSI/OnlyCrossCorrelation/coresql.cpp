//============================================================================
// Name        : coresql.cpp
// Author      : Maria
// Version     : v.01
// Copyright   : Your copyright notice
// Description : Core + SQL connection + Preprocessing + Crosscorrelation
//============================================================================

#include <iostream>
using namespace std;

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <ctime>
#include <string>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <thread>

#ifdef WIN32
#include <windows.h>          // For ::Sleep()
void sleep(unsigned int seconds) {::Sleep(seconds * 1000);}
#else
#include <unistd.h>           // For sleep()
#endif

#include "csql.h"
#include "communication.h"
#include "zlib.h"

float *myPreProcessing;

using namespace std;

/*typedef struct package{
	int number;
	float *data;
}pack;*/


void DateAddSeconds( struct tm* date, int segundos )
{
    // Seconds since start of epoch
    time_t date_seconds = mktime( date ) + ( segundos) ;

    // Update caller's date
    // Use localtime because mktime converts to UTC so may change date
    *date = *localtime( &date_seconds ) ;
}

string arrangedate(string oldtimeStamp, int secondsOfData){
	int year,month,day,hour,minute,sec;
	time_t now = time(0);
   	struct tm *date = localtime(&now);
	string newtimeStamp;

	separateTimestamp(oldtimeStamp,year,month,day,hour,minute,sec);

	date->tm_year=year-1900;
	date->tm_mon=month-1;
	date->tm_mday=day;
	date->tm_hour=hour;
	date->tm_min=minute;
	date->tm_sec=sec;

	DateAddSeconds(date,secondsOfData);

	string monthc = to_string(date->tm_mon+1);
	if(monthc.length()<2) monthc = "0" + monthc;
	string dayc = to_string(date->tm_mday);
	if(dayc.length()<2) dayc = "0" + dayc;
	string hourc = to_string(date->tm_hour);
	if(hourc.length()<2) hourc = "0" + hourc;
	string minc = to_string(date->tm_min);
	if(minc.length()<2) minc = "0" + minc;
	string secc = to_string(date->tm_sec);
	if(secc.length()<2) secc = "0" + secc;
	newtimeStamp = to_string(date->tm_year+1900) + monthc + dayc + hourc + minc + secc;	

	return newtimeStamp;

}



int main(int argc,char *argv[]) {
	

	pack packagesend;
	string dbName,ipHostMachine,userDb,passwordDb,configurationFile,timeStamp;
	int nodeNumber,secondsOfData;
	if (argc!=7 && argc!=8){
		cout<<"Usage: [nodeNumber] [ipHostMachine] [userDb] [passwordDb] [configurationFile] [timeStamp (YearMonthDayHourMinuteSecond)] [secondOfData] \n"<<endl;
	    return 1;
	}
	nodeNumber=atoi(argv[1]);
	ipHostMachine=argv[2];
	userDb=argv[3];
	if(argc==7){
		passwordDb="";
	    configurationFile=argv[4];
	    timeStamp=argv[5];
	    secondsOfData=atoi(argv[6]);
	}
	else{
		passwordDb=argv[4];
		configurationFile=argv[5];
		timeStamp=argv[6];
		secondsOfData=atoi(argv[7]);
	}



	dbName=nodeRealName(nodeNumber, configurationFile);

	int datasize,samplingRate;
	int block=1;		//Block of minutes counter

	//std::string destAddress = "localhost";
	std::string destAddress = "172.16.255.255";
	unsigned short destPort = 5000;	

	
	myPreProcessing=readInfoDatabase(ipHostMachine, userDb, passwordDb, dbName,timeStamp,secondsOfData,datasize,samplingRate);
	packagesend.number=block;
	packagesend.data = myPreProcessing;
	//setData(myPreProcessing);

	string myname = "cross/" + to_string(block) + "_" + to_string(nodeNumber);
	FILE *f;
	f = fopen(myname.c_str(),"wb");
        if(f){
		fwrite(myPreProcessing,sizeof(float),sizeof(float)*datasize,f);
		fclose(f);
	}

	float *redata = new float[datasize];
	std::thread t_recv(&receive_UDP,destPort,samplingRate, redata, datasize);
	t_recv.detach();
	
	send_UDP2(destAddress,destPort,samplingRate, packagesend, datasize);

	int i;
	for(i=2;i<=55;i++){

		timeStamp = arrangedate(timeStamp,secondsOfData);
	}
	for(;i<=3000;i++){

		timeStamp = arrangedate(timeStamp,secondsOfData);
	
		block++;
		myPreProcessing=readInfoDatabase(ipHostMachine, userDb, passwordDb, dbName,timeStamp,secondsOfData,datasize,samplingRate);
		packagesend.number=block;
		packagesend.data = myPreProcessing;
		//setData(myPreProcessing);

		myname = "cross/" + to_string(block) + "_" + to_string(nodeNumber);
		string myname = "cross/" + to_string(block) + "_" + to_string(nodeNumber);

		f = fopen(myname.c_str(),"wb");
        	if(f){
			fwrite(myPreProcessing,sizeof(float),sizeof(float)*datasize,f);
			fclose(f);
		}
	
		sleep(2);
		cout<<"Timestamp here:"<<timeStamp<<endl;
		send_UDP2(destAddress,destPort,samplingRate, packagesend, datasize);
		sleep(2);

	}
				    	
		    	

		


	sleep(15);
	
	
	cout << "!!!Finish!!!" << endl; 
	return 0;
}



