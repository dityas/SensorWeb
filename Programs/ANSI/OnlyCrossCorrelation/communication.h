/*
 * communication.h
 *
 *  Created on: Apr 6, 2017
 *      Author: maria
 */

#ifndef COMMUNICATION_H_
#define COMMUNICATION_H_

#include <iostream>
using namespace std;

typedef struct package{
	int number;
	float *data;
}pack;


int recv_list(char neighbor_ips[][20]);
void obtainNumberNode(char *raw_serv);
void send_UDP2(string destAddress,unsigned short destPort,int samplingRate, pack package, int sizedata);
void receive_UDP(unsigned short echoServPort, int samplingRate, float data[],int sizedata);
unsigned char * compression(float *arraySend,int elements, int &tambuf);
float * uncompression(unsigned char *buf, int tambuf, int elements);
int separateSourceAddress(string source);
int myNeighborNumber(const char *name);

#endif /* COMMUNICATION_H_ */
