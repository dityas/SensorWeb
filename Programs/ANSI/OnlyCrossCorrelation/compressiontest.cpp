#include <iostream>
using namespace std;

#include <stdlib.h>
#include <stdio.h>
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


#include "zlib.h"

using namespace std;

int main(int argc,char *argv[]) {

	float original[10] = {-0.12569,2.25698,-1.25652,2.222,3.33333,4,3,2,1,0};
	
	int tam = sizeof(original);
	cout<<"Tam: "<<tam<<endl;

	//compress

	unsigned char *ori = new unsigned char[tam];
	memcpy(ori,&original,tam);

	cout<<ori<<endl;

	unsigned char *buf;
	unsigned long buflen;
	unsigned long slen = tam +1;
	buflen = compressBound(slen);
	buf = (unsigned char*)malloc(sizeof(unsigned char)*buflen);
	compress(buf, &buflen, (const Bytef *)ori, slen);

	cout<<buflen<<endl;
	cout<<sizeof(buf)<<endl;

	//uncompress

	unsigned char *dec_buf;
	dec_buf = (unsigned char*)malloc(sizeof(unsigned char)*buflen);
//	dec_buf = (unsigned char*)malloc(tam);
	
	uncompress(dec_buf, &slen, buf, buflen); 
	
	cout<<"UC: "<<dec_buf<<endl;

	float after[10];
	memcpy(&after,dec_buf,sizeof(after));

	for(int i=0 ; i<10;i++)
		cout<<after[i]<<endl;


	

	cout << "!!!Finish!!!" << endl; 
	return 0;
}

