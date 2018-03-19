/*
 * csql.h
 *
 *  Created on: Mar 31, 2017
 *      Author: maria
 */


#ifndef CSQL_H_
#define CSQL_H_

#include <iostream>

#include "fft.h"
using namespace std;




void separateTimestamp(string timeStamp, int &year, int &month, int &day, int &hour, int &minute, int &sec);
float* readInfoDatabase(string ipAddress, string dbUser, string dbPassword,string dbName, string timeStamp, int secondsOfData,int &datasize, int &sampling);
string nodeRealName(int nodeNumber, string confFile);
void taper(float *data,int nt,int lramp);
void whitening(complex data[],int size);
void instrument(float *data,int nt);
void prepareCorrelation(int block, int sizedata, const char *newname);
void setData(float *dataToSet);
void cross(complex data1[],complex data2[],complex cor[],int nt);
void FreqWhitening(complex data[],int size);
void TimeWhitening(float data[],int size);

#endif /* CSQL_H_ */
