/*
 * csql.cpp
 *
 *  Created on: Mar 31, 2017
 *      Author: maria
 */
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <mysql_connection.h>
#include <iomanip>
#include <fstream>

#include <driver.h>
#include <exception.h>
#include <resultset.h>
#include <statement.h>

#include "valveSql.h"
#include "communication.h"
#include "fft.h"

float *myData;


/*******LIBRARIES FOR FFT******************************/

void conjugate_complex(int n,complex in[],complex out[])
{
  int i = 0;
  for(i=0;i<n;i++)
  {
    out[i].imag = -in[i].imag;
    out[i].real = in[i].real;
  }
}

void c_abs(complex f[],float out[],int n)
{
  int i = 0;
  float t;
  for(i=0;i<n;i++)
  {
    t = f[i].real * f[i].real + f[i].imag * f[i].imag;
    out[i] = sqrt(t);
  }
}


void c_plus(complex a,complex b,complex *c)
{
  c->real = a.real + b.real;
  c->imag = a.imag + b.imag;
}

void c_sub(complex a,complex b,complex *c)
{
  c->real = a.real - b.real;
  c->imag = a.imag - b.imag;
}

void c_mul(complex a,complex b,complex *c)
{
  c->real = a.real * b.real - a.imag * b.imag;
  c->imag = a.real * b.imag + a.imag * b.real;
}

void c_div(complex a,complex b,complex *c)
{
  c->real = (a.real * b.real + a.imag * b.imag)/(b.real * b.real +b.imag * b.imag);
  c->imag = (a.imag * b.real - a.real * b.imag)/(b.real * b.real +b.imag * b.imag);
}

#define SWAP(a,b)  tempr=(a);(a)=(b);(b)=tempr

void Wn_i(int n,int i,complex *Wn,char flag)
{
  Wn->real = cos(2*PI*i/n);
  if(flag == 1)
  Wn->imag = -sin(2*PI*i/n);
  else if(flag == 0)
  Wn->imag = -sin(2*PI*i/n);
}


void fft(int N,complex f[])
{
  complex t,wn;
  int i,j,k,m,n,l,r,M;
  int la,lb,lc;

  for(i=N,M=1;(i=i/2)!=1;M++);

  for(i=1,j=N/2;i<=N-2;i++)
  {
    if(i<j)
    {
      t=f[j];
      f[j]=f[i];
      f[i]=t;
    }
    k=N/2;
    while(k<=j)
    {
      j=j-k;
      k=k/2;
    }
    j=j+k;
  }


  for(m=1;m<=M;m++)
  {
    la=pow(2,m);
    lb=la/2;

    for(l=1;l<=lb;l++)
    {
      r=(l-1)*pow(2,M-m);
      for(n=l-1;n<N-1;n=n+la)
      {
        lc=n+lb;
        Wn_i(N,r,&wn,1);
        c_mul(f[lc],wn,&t);
        c_sub(f[n],t,&(f[lc]));
        c_plus(f[n],t,&(f[n]));
      }
    }
  }
}


void ifft(int N,complex f[])
{
  int i=0;
  conjugate_complex(N,f,f);
  fft(N,f);
  conjugate_complex(N,f,f);
  for(i=0;i<N;i++)
  {
    f[i].imag = (f[i].imag)/N;
    f[i].real = (f[i].real)/N;
  }
}

int nextpower2(int n)
   {
	int n2;
	n2= 1;
	while(n2 <= n) n2 *= 2;
	return(n2);
   }

/*******END LIBRARIES FOR FFT******************************/


using namespace std;

void separateTimestamp(string timeStamp, int &year, int &month, int &day, int &hour, int &minute, int &sec){
	year=atoi(timeStamp.substr(0,4).c_str());
	month=atoi(timeStamp.substr(4,2).c_str());
	day=atoi(timeStamp.substr(6,2).c_str());
	hour=atoi(timeStamp.substr(8,2).c_str());
	minute=atoi(timeStamp.substr(10,2).c_str());
	sec=atoi(timeStamp.substr(12,2).c_str());

}

void taper(float *data,int nt,int lramp){
	double dwt, wt;
	int i;
   	dwt= 1.0/(lramp);
	wt= 0.0;
	for(i=0; i<lramp; i++){
	   	data[i] *= wt;
		data[nt-i-1] *= wt;
		wt += dwt;
	}
}

void whitening(complex data[],int size)
{
	float temp_max=0.0;
	int i;
	fft(size,data);	  
	for(i=0;i<size;i++)
	{
	if(temp_max<(data[i].real*data[i].real+data[i].imag*data[i].imag))
		temp_max=(data[i].real*data[i].real+data[i].imag*data[i].imag);
	}
	temp_max=sqrt(temp_max);
	for(i=0;i<size;i++)
	{
	data[i].real=data[i].real/temp_max;
	data[i].imag=data[i].imag/temp_max;
	}

}

void instrument(float *data,int nt)
{
	float mean=0;
	int i;
	for(i=0; i<nt; i++)
	   {
	   	mean += data[i];		
	   }
  	 mean=mean/nt;
	for(i=0; i<nt; i++)
	   {
	   	data[i]=data[i]-mean;		
	   }
}

int downsampling(float *data,int nt,int rate)
   {
    float mean=0;
    float *data1;
    int count=0;
    data1 = new float[(int)nt/rate];
    int i,j;
    for(i=0; i<nt;i+=rate)
       {    mean=0;
        for(j=0;j<rate;j++)
           {
         mean=mean+data[i+j];
         data1[(int)i/rate]=mean/rate;
        }
	count++;
       }

    for(i=0;i<count;i++){
    	data[i]=data1[i];
    }
    return count;
}

void FreqWhitening(complex data[],int size)
{
float *temp_max;
temp_max=new float[size];
int i,j;
	fft(size,data);	  
	for(i=0;i<size;i++)
	{
		temp_max[i]=0;
		for(j=i-100;j<i+100;j++)
		{if(j<0||j>=size)
			;
		else if(temp_max[i]<sqrt(data[j].real*data[j].real+data[j].imag*data[j].imag))
			temp_max[i]=sqrt(data[j].real*data[j].real+data[j].imag*data[j].imag);
				
		}

	}
	//    	for(int j = 0 ; j < size ; j++)
	//		cout << temp_mean[j] << endl;
	for(i=0;i<size;i++)
	{
		if(temp_max[i]!=0)
		{data[i].real=data[i].real/temp_max[i];
		data[i].imag=data[i].imag/temp_max[i];}
	}

}

void TimeWhitening(float data[],int size)
{
float temp_max=0.0;
int i;	  
	for(i=0;i<size;i++)
	{
	if(temp_max<data[i])
		temp_max=data[i];
	}
	if(temp_max!=0)
	{for(i=0;i<size;i++)
	{
	data[i]=data[i]/temp_max;
	}
	}

}



float* readInfoDatabase(string ipAddress, string dbUser, string dbPassword,string dbName,string timeStamp,int secondsOfData,int &datasize, int &sampling){

	int lramp=1000;
	int year,month,day,hour,minute,sec;
	separateTimestamp(timeStamp,year,month,day,hour,minute,sec);
	int* data = NULL;
	int size,samplingRate;
	cout<<"Reading from: "<<dbName<<endl;

	readDataFromValve(ipAddress, dbUser, dbPassword, dbName, year, month, day, hour, minute, sec, secondsOfData, &data, size , samplingRate);

	cout<<endl;


	//Sili code	
	int winsize = size;	//Because I'm only reading 5 min data
	
	cout<<"******Data Information******"<<endl;
	cout<<"Window Size: "<<winsize<<endl;
	
	float *data1;
	data1 = new float[winsize];

	
	
	for(int j=0;j<winsize;j++)
	{  
		data1[j]=(float)data[j];
        }
	//Downsampling
	int rate = 5;//winsize/samplingRate/60;
	cout<<"Rate: "<<rate<<endl;
	winsize = downsampling(data1,winsize,rate);
	cout<<"winsize after downsampling: "<<winsize<<endl;


	int nsize;
	nsize=nextpower2(winsize);
	cout<<"Size Power2: "<<nsize<<endl;

	struct complex *data2;
	float *result;
	data2 = new struct complex[nsize];
	result = new float[nsize];


	//Instrument noise removing
	instrument(data1,winsize);
	//Taper process	
	taper(data1,winsize,lramp);

	
	for(int j=0;j<winsize;j++){
		data2[j].real=data1[j];
		data2[j].imag=0;
	}
	for(int j=winsize;j<nsize;j++){
		data2[j].real=0;
		data2[j].imag=0;
	}

	//Frequency Whitening process
	FreqWhitening(data2,nsize);

 	for(int i = 0 ; i < nsize ; i++){
		result[i]=data2[i].real;
	}
	datasize = nsize;
	sampling = samplingRate;

	

	cout<<"********"<<endl;	
	FILE *ff;
	ff=fopen("swdata_fd.dat","w");
	for(int i = 0 ; i < datasize ; i++)
	 	fprintf(ff,"%f\n",result[i]);
	fclose(ff);

	cout<<"********"<<endl;

	return result;


	//Test to send raw data	//Conclusion here: if we transfer time domain data, we can transfer 4 minutes. In frequency domain it will be 2 minutes.
	//datasize=winsize;
	//return data1;


}

string nodeRealName(int nodeNumber, string confFile){


	FILE *f;
	int num;
	char type[500];
	string realName;

	f=fopen(confFile.c_str(),"r");
	if(f!=NULL){
		while(!feof(f)){
			fscanf(f,"%d %s",&num,type);
			if(num==nodeNumber)
				realName = type;
		}
		fclose(f);
	}
	return  realName;
}

int myNeighborNumber(const char *name){
	string source = name;	
	string n;
	n=source.substr(source.find_last_of("_")+1);
	int number = atoi(n.c_str());
	return number;
}

void cross(complex data1[],complex data2[],complex cor[],int nt)
{
	int i;
        for(i=0; i<nt; i++)
	   {
	     cor[i].real=  data1[i].real * data2[i].real
	       + data1[i].imag * data2[i].imag;
	     cor[i].imag=  data1[i].imag * data2[i].real
	       - data1[i].real * data2[i].imag;
	   }

}


void prepareCorrelation(int block, int sizedata, const char *newname){
	
	
	//My data is inside myData vector
	//My neighbor data is inside myNeigData vector

	float *myNeigData = new float[sizedata];
	float *myOwnData = new float[sizedata];
	int myNN;
	myNN=myNeighborNumber(newname);
	int sw=0;

	char number[10];
	int myID;
	obtainNumberNode(number);
	myID = atoi(number);

	cout<<"****STARTING CROSSCORRELATION BETWEEN "<<myID<<" AND "<<myNN<<" USING BLOCK "<<block<<"****"<<endl;

	string myname = "cross/" + to_string(block) + "_" + to_string(myID);
	
	FILE *f;
	f=fopen(newname,"rb");
	if(f){
		fread (myNeigData, 1, sizeof(float)*sizedata, f);
		fclose(f);
	}
	else{	cout<<"Error correlating data with node "<<myNN<<endl;
		sw=1;
	}
	f=fopen(myname.c_str(),"rb");
	if(f){
		fread (myOwnData, 1, sizeof(float)*sizedata, f);
		fclose(f);
	}
	else{	cout<<"Error correlating data with node "<<myNN<<endl;
		sw=1;
	}

	struct complex *data1;
	struct complex *data2;
	struct complex *cor;
	float *cortime = new float[sizedata];

	//Here if we use time domain this has to be converted to freq domain and the size change	

	data1 = new struct complex[sizedata];
	data2 = new struct complex[sizedata];
	cor = new struct complex[sizedata];

	for(int i=0;i<sizedata;i++){
		data1[i].real = myOwnData[i];
		data1[i].imag = 0;
		data2[i].real = myNeigData[i];
		data2[i].imag = 0;
	}

	cross(data1,data2,cor,sizedata);
	ifft(sizedata,cor);

	for(int i = 0 ; i < sizedata ; i++)
		cortime[i]=cor[i].real;
	TimeWhitening(cortime,sizedata);

if(sw==0){
	
	for(int z = 0 ; z < 10 ; z++)
			cout << cortime[z] << endl ;
	cout << sizedata << endl;
	
	//Stacking process

	

	FILE *fc;
	string path = "cross/CC" + to_string(myID) + "_" + to_string(myNN);
	string path2 = "cross/N" + to_string(myID) + "_" + to_string(myNN);
	float *cortimeNN = new float[sizedata];
	float *add = new float[sizedata];
	int times=0;
	fc=fopen(path.c_str(),"rb");
	if(fc){								//Option 3. There are previous results
		fread (cortimeNN, 1, sizeof(float)*sizedata, fc);
		fclose(fc);
		for(int i=0;i<sizedata;i++)
			add[i] = (cortime[i] + cortimeNN[i]);
		fc = fopen(path.c_str(),"wb");
		fwrite(add,sizeof(float),sizeof(float)*sizedata,fc);
		fclose(fc);

		fc = fopen(path2.c_str(),"r");
		fscanf(fc,"%d",&times);
		fclose(fc);
		fc = fopen(path2.c_str(),"w");
		times = times + 1;
		cout<<"TIME---->>>>"<<times<<endl;
		fprintf(fc,"%d",times);
		fclose(fc);
		
		
	}else{								//Option 1. There are NOT previous results
		fc = fopen(path.c_str(),"wb");
		fwrite(cortime,sizeof(float),sizeof(float)*sizedata,fc);
		fclose(fc);
		
		fc = fopen(path2.c_str(),"w");
		fprintf(fc,"%d",1);
		fclose(fc);
		cout<<"TIME---->>>> 1"<<endl;
	}
}

	//remove(newname);

	//write on VALVE for testing only
	/*if(myID==1 && myNN==2 && block == 4320){
		cout<<"Datasize: "<<sizedata<<endl;
		int value[12000]={0};
		cout<<"***To write crosscorrelation in VALVE****"<<endl;
		for(int i=0;i<12000;i++){
			value[i] = (cortime[i]/4320)*100000000;
			cout<<cortime[i]<<"----->"<<value[i]<<endl;
		}
		removeDataBaseValve("172.16.0.254", "oasis", "",  "CC1");
		sleep(3);
		writeDataToValve("172.16.0.254", "oasis", "",  "CC1", 2014 , 3, 21, 0, 0, 0, value, 12000, 100);
		cout<<"Finish to write"<<endl;

	}*/

	
	
	
}

void setData(float *dataToSet){
	myData = dataToSet;
}




