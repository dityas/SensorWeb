/*
 * communication.cpp
 *
 *  Created on: Apr 6, 2017
 *      Author: maria
 */

#include "PracticalSocket.h"  // For UDPSocket and SocketException
#include "zlib.h"
#include <iostream>           // For cout and cerr
#include <cstdlib>            // For atoi()
#include <string.h>
#include <sys/stat.h>

#include <thread>

#ifdef WIN32
#include <windows.h>          // For ::Sleep()
void sleep(unsigned int seconds) {::Sleep(seconds * 1000);}
#else
#include <unistd.h>           // For sleep()
#endif

#include "csql.h"

using namespace std;
const int MAXRCVSTRING = 65527;



typedef struct package{
	int number;
	float *data;
}pack;


int recv_list(char neighbor_ips[][20])
{
	char raw_serv[20];
	int len;
	FILE *fp;  
	fp = popen("ip route  | awk -F\" \" '{ if($3 ==\"eth0\" && $1!=\"172.16.0.0/24\") print $1 }'|sort -R", "r");
	int count=0;	
	while(fgets(raw_serv,20,fp)!=NULL)
	{
	   len=strlen(raw_serv)-1;
	   raw_serv[len]='\0';
	   strcpy(neighbor_ips[count],raw_serv);	   
	   count++;				
	}
	pclose(fp);
	return count;
}

void obtainNumberNode(char *raw_serv){
	FILE* fp= popen("pwd | grep -Eo '[[:digit:]]+' | tail -n1","r");
	fgets(raw_serv,20,fp);
	pclose(fp);
	
}

unsigned char * compression(float *arraySend,int elements, int &tambuf){
	cout<<"****Starting compression*****"<<endl;
	int tam = elements * sizeof(float);
	cout<<"Original size: "<<tam<<endl;
	unsigned char *ori = new unsigned char[tam];
	memcpy(ori,arraySend,tam);

	unsigned char *buf;
	unsigned long buflen;
	unsigned long slen = tam +1;
	buflen = compressBound(slen);
	
	buf = new unsigned char[buflen];
	compress(buf, &buflen, (const Bytef *)ori, slen);
	
	tambuf = buflen;
	cout<<"Compressed Size: "<<tambuf<<endl;

	free(ori);
	
	return buf;

}

unsigned char * uncompression(unsigned char *buf, int tambuf, int elements){

	cout<<"****Starting uncompression*****"<<endl;
	unsigned char *dec_buf;
	unsigned long buflen = (unsigned long) tambuf;
	
	dec_buf = new unsigned char[tambuf];
	
	uncompress(dec_buf, &buflen, buf, buflen); 

	return dec_buf;
}

int separateSourceAddress(string source){
	string n;	
	n=source.substr(source.find_last_of(".")+1);
	int number = atoi(n.c_str());
	return number;
}

void send_UDP2(string destAddress,unsigned short destPort,int samplingRate, pack package, int sizedata){

	cout<<"Block Number: "<<package.number<<endl;
	
	unsigned char *compressedArray;
	int sizeCompressed;
	
	compressedArray = compression(package.data,sizedata,sizeCompressed);

	
	int size = sizeCompressed; 
	//New part
	unsigned char *newsend = new unsigned char[sizeCompressed + sizeof(float)];
	memcpy(newsend,&package.number,sizeof(package.number));
	cout<<"Convertion: "<<newsend<<endl;
	memcpy(newsend + sizeof(package.number),compressedArray,sizeCompressed);

	size = size + sizeof(int);
	
	try {
    		UDPSocket sock;
   		for (int i=0;i<2;i++) {
			cout<<"Sending bytes: "<<size<<endl;
				sock.sendTo(newsend, size, destAddress, destPort);
		
				for(int i=0;i<10;i++)
    					cout << "Sending " << package.data[i] << endl;
      			sleep(3);
    		}
  	} catch (SocketException &e) {
    		cerr << e.what() << endl;
    		exit(1);
  	}
}

void receive_UDP(unsigned short echoServPort,int samplingRate, float data[], int sizedata){

	try {
    		UDPSocket sock(echoServPort);

		unsigned char *uncompressedarray;
		unsigned char *rec;

    		
   		
    		rec = new unsigned char[MAXRCVSTRING];
    		string sourceAddress;              // Address of datagram source
    		unsigned short sourcePort;         // Port of datagram source
    		int size=MAXRCVSTRING;

    		for (;;) {
    			int bytesRcvd = sock.recvFrom(rec, size, sourceAddress, sourcePort);
			cout<<"Bytes receive: "<<bytesRcvd<<endl;

			if(bytesRcvd>0){

				int a;
				int sizeCompressed = bytesRcvd - sizeof(int);
				unsigned char *reverse = new unsigned char[sizeCompressed];
				memcpy((char*)&a,rec,sizeof(4));
				memcpy(reverse,rec+sizeof(4),sizeCompressed);
				
				cout<<"****Starting uncompression of "<<sourceAddress<<"*****"<<endl;
				uncompressedarray = uncompression(reverse,sizeCompressed,sizedata);

				//Write the information
				char number[10];
				int myID;
				obtainNumberNode(number);
				myID = atoi(number);

				float *after = new float[sizedata];
				memcpy(after,uncompressedarray,(sizedata*sizeof(float)));
				cout<<"Timestamp: "<<a<<endl;
				if(separateSourceAddress(sourceAddress) != myID){
					for(int i=0;i<10;i++){
						cout << "Received " << after[i] << " from " << sourceAddress << ": "<< sourcePort << endl;
					}
				}

				
		
				if(separateSourceAddress(sourceAddress) != myID){
		
					string newname;
					string path = "cross/temp" + to_string(a) + "_" + to_string(separateSourceAddress(sourceAddress));

					FILE *fe;
					fe = fopen(path.c_str(),"rb");
					if(!fe){
						FILE *tf;
						tf=fopen(path.c_str(),"wb");
						if(tf){
							fwrite (after , sizeof(float), sizeof(float)*sizedata, tf);
							fclose(tf);
							newname = "cross/" + to_string(a) + "_" + to_string(separateSourceAddress(sourceAddress));
							FILE *f;
							f=fopen(newname.c_str(),"rb");
							if(!f){						
								rename(path.c_str(),newname.c_str());
								std::thread t_corr(&prepareCorrelation,a,sizedata,newname.c_str());	
								t_corr.detach();
								//t_corr.join();
							}else{
								fclose(f);
							}
						}else{cout<<"Error writing temporal file of "<<path<<endl;}
					}else{
			 			fclose(fe);}
					remove(path.c_str());
				
				}
			}

		}
  	} catch (SocketException &e) {
    		cerr << e.what() << endl;
    		exit(1);
  	}


}




