#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <cstdlib>
#include <ctime>
#include <mysql_connection.h>
#include <iomanip>

#include <driver.h>
#include <exception.h>
#include <resultset.h>
#include <statement.h>

using namespace std;

void readDataFromValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int secondsOfData, int** data, int &size, int &samplingRate){
	std::string temporalTable;
	std::string f;
    std::string temporal = "a";
    std::string script = "java -jar javaReader.jar  ";
    char buffer[500];
    std::string strBuff;
    char nameRan[10];

    srand(time(0));

    int fileRam = rand() % 30444 + 20000;


    sprintf(nameRan, "%d", fileRam);
    temporal = temporal+nameRan;

    sprintf(buffer, " %d %d %d %d %d %d %d ", year,month,day,hour,minute,second,secondsOfData);
    strBuff = buffer;

    script = script + ipAddress + " " + dbUser + " " + dbPassword + " " + dbName + " " + temporal +  " " + strBuff + " 1";
 //   cout << endl << script << endl;
    // "java -jar javaReader.jar  msi\\$st1\\$e "+ temporal + " 2014 10 1 15 0 0 35"
	system(script.c_str());

	temporal = temporal+".dat";
	FILE *fp = fopen(temporal.c_str(),"rb+");
    if(fp==NULL)
    	cout << "No Data";
    else{
    	fseek(fp, 0L, SEEK_END);
    	size = ftell(fp);
    	rewind(fp);

    	size = size/4;

        *data = (int *)malloc (sizeof (int)*size);

        fread(*data,4,size,fp);


	fclose(fp);
    remove(temporal.c_str());
    }


	temporal = temporal+".sr";
	fp = fopen(temporal.c_str(),"r");

	fscanf(fp,"%d",&samplingRate);

	fclose(fp);
	remove(temporal.c_str());

}

//void writeDataToValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int samplingRate, int totalSamples, int data[]);
void writeDataToValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int data[], int size, int samplingRate){
    std::string script = "java -jar javaReader.jar  ";
    std::string temporal = "a";
    char buffer[500];
    std::string strBuff;
    char nameRan[10];

    int totalSamples = size;
    srand(time(0));

    int fileRam = rand() % 30444 + 20000;
    sprintf(nameRan, "%d.dat", fileRam);

    temporal = temporal+nameRan;

    sprintf(buffer, " %d %d %d %d %d %d %d ", year,month,day,hour,minute,second,samplingRate);
    strBuff = buffer;

    script = script + ipAddress + " " + dbUser + " " + dbPassword + " " + dbName + " " + temporal +  " " + strBuff + " 2";

    FILE *fp = fopen(temporal.c_str(),"wb");

    if(fp==NULL)
      	cout << "Error temporal data";
    else{
    	fwrite(data,4,totalSamples,fp);
    }

    fclose(fp);

   // cout << script;
    system(script.c_str());

}


void removeDataBaseValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName){
    std::string script = "java -jar javaReader.jar  ";

    script = script + ipAddress + " " + dbUser + " " + dbPassword + " " + dbName + " 3";
	system(script.c_str());

}

void readStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, double &longitude, double &latitude, double &z, double &scaler){
    FILE *fp;

    std::string script = "java -jar javaReader.jar  ";

    script = script + ipAddress + " " + dbUser + " " + dbPassword + " " + dbName + " 4";
	system(script.c_str());


    fp = fopen("station.dat","r");

    fscanf(fp,"%lf %lf %lf %lf",&longitude,&latitude,&z,&scaler);

    fclose(fp);

    remove("station.dat");
}

void writePickingToValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int millisecond, float amplitude){
     std::string script = "java -jar javaReader.jar  ";
     char buffer[500];
     std::string strBuff;

     sprintf(buffer, " %.8f %d %d %d %d %d %d %d", amplitude, year,month,day,hour,minute,second,millisecond);

     strBuff = buffer;
     script = script + ipAddress + " " + dbUser + " " + dbPassword + " " + dbName + " " + strBuff + " 5";

     system(script.c_str());
}

void createInfoDatabase(std::string ipAddress, std::string dbUser, std::string dbPassword,std::string dbName){
	try{
		      sql::Driver *driver;
		  	  sql::Connection *con;
		  	  sql::Statement *stmt;
		  	  sql::ResultSet *res;

		  	  /* Create a connection */
		  	  driver = get_driver_instance();
		  	  con = driver->connect(ipAddress, dbUser, dbPassword);

			  con->setSchema("INFORMATION_SCHEMA");
			  stmt = con->createStatement();
			  res  = stmt->executeQuery("SELECT count(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '"+dbName+"'");

			  res->next();
			  int dbExists = (res->getInt(1));

			  if( dbExists < 1){
				  stmt->executeUpdate("CREATE DATABASE "+dbName+"");
			  }

			      delete res;
			  	  delete stmt;
			  	  delete con;

	       	   }catch (sql::SQLException &e) {
	       		   cout << "# ERR: SQLException in " << __FILE__;
	       		   cout << "# ERR: " << e.what();
	       		   cout << " (MySQL error code: " << e.getErrorCode();
	       		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
	           }

}

void writeEventLocation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName, int year, int month, int day, int hour, int minute, int second, int millisecond, float lng,float lat,float z,float magnitude){
	      using namespace sql;

	      std::string dbName = "w_" + deploymentName + "$info";

	    try{
	      sql::Driver *driver;
	  	  sql::Connection *con;
	  	  sql::Statement *stmt;

	  	  createInfoDatabase(ipAddress, dbUser, dbPassword,dbName);

	  	  /* Create a connection */
	  	  driver = get_driver_instance();
	  	  con = driver->connect(ipAddress, dbUser, dbPassword);

		  con->setSchema(dbName);
		  stmt = con->createStatement();


		  stmt->executeUpdate("create table IF NOT EXISTS location(time timestamp(6),lng float(9,6),lat float(9,6),z float(6,3), magnitude float(6,3));");
			 // stmt->executeUpdate("create table station(name varchar(20),lng float(9,6),lat float(9,6));");


		  std::string strBuff;
		  char buffer[500];

		  sprintf(buffer, "insert into location values ('%d-%d-%d %d:%d:%d.%d',%f,%f,%f,%f);", year,month,day,hour,minute,second,millisecond,lng,lat,z,magnitude);
		  strBuff = buffer;

		  stmt->executeUpdate(strBuff);

		  	  delete stmt;
		  	  delete con;

       	   }catch (sql::SQLException &e) {
       		   cout << "# ERR: SQLException in " << __FILE__;
       		   cout << "# ERR: " << e.what();
       		   cout << " (MySQL error code: " << e.getErrorCode();
       		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
           }

}


void writeStationLocation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName, std::string stationName, float lng,float lat,float depth){
    using namespace sql;

    std::string dbName = "w_" + deploymentName + "$info";

  try{
      sql::Driver *driver;
	  sql::Connection *con;
	  sql::Statement *stmt;


	  /* Create a connection */
	  driver = get_driver_instance();
	  con = driver->connect(ipAddress, dbUser, dbPassword);

	  con->setSchema(dbName);
	  stmt = con->createStatement();


	  stmt->executeUpdate("create table IF NOT EXISTS station(name varchar(20),lng float(9,6),lat float(9,6),depth float(9,6));");

	  std::string strBuff;
	  char buffer[500];

	  sprintf(buffer, "delete from station where name = '%s';", stationName.c_str());
	  strBuff = buffer;

	  stmt->executeUpdate(strBuff);

	  sprintf(buffer, "insert into station values ('%s',%f,%f,%f);", stationName.c_str(),lng,lat,depth);
	  strBuff = buffer;

	  stmt->executeUpdate(strBuff);

	  	  delete stmt;
	  	  delete con;

 	   }catch (sql::SQLException &e) {
 		   cout << "# ERR: SQLException in " << __FILE__;
 		   cout << "# ERR: " << e.what();
 		   cout << " (MySQL error code: " << e.getErrorCode();
 		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
     }

}

void removeStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName, std::string stationName){
    using namespace sql;

    std::string dbName = "w_" + deploymentName + "$info";

  try{
    sql::Driver *driver;
	  sql::Connection *con;
	  sql::Statement *stmt;


	  createInfoDatabase(ipAddress, dbUser, dbPassword,dbName);

	  /* Create a connection */
	  driver = get_driver_instance();
	  con = driver->connect(ipAddress, dbUser, dbPassword);

	  con->setSchema(dbName);
	  stmt = con->createStatement();


	  stmt->executeUpdate("create table IF NOT EXISTS station(name varchar(20),lng float(9,6),lat float(9,6));");

	  std::string strBuff;
	  char buffer[500];

	  sprintf(buffer, "delete from station where name = '%s';", stationName.c_str());
	  strBuff = buffer;

	  stmt->executeUpdate(strBuff);

	  	  delete stmt;
	  	  delete con;

 	   }catch (sql::SQLException &e) {
 		   cout << "# ERR: SQLException in " << __FILE__;
 		   cout << "# ERR: " << e.what();
 		   cout << " (MySQL error code: " << e.getErrorCode();
 		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
     }

}

void removeAllStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName){
    using namespace sql;

    std::string dbName = "w_" + deploymentName + "$info";

  try{
    sql::Driver *driver;
	  sql::Connection *con;
	  sql::Statement *stmt;


	  createInfoDatabase(ipAddress, dbUser, dbPassword,dbName);

	  /* Create a connection */
	  driver = get_driver_instance();
	  con = driver->connect(ipAddress, dbUser, dbPassword);

	  con->setSchema(dbName);
	  stmt = con->createStatement();


	  stmt->executeUpdate("create table IF NOT EXISTS station(name varchar(20),lng float(9,6),lat float(9,6));");

	  std::string strBuff;
	  char buffer[500];

	  sprintf(buffer, "delete from station;");
	  strBuff = buffer;

	  stmt->executeUpdate(strBuff);

	  	  delete stmt;
	  	  delete con;

 	   }catch (sql::SQLException &e) {
 		   cout << "# ERR: SQLException in " << __FILE__;
 		   cout << "# ERR: " << e.what();
 		   cout << " (MySQL error code: " << e.getErrorCode();
 		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
     }

}

void removeAllEvents(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName){
    using namespace sql;

    std::string dbName = "w_" + deploymentName + "$info";

  try{
      sql::Driver *driver;
	  sql::Connection *con;
	  sql::Statement *stmt;


	  createInfoDatabase(ipAddress, dbUser, dbPassword,dbName);

	  /* Create a connection */
	  driver = get_driver_instance();
	  con = driver->connect(ipAddress, dbUser, dbPassword);

	  con->setSchema(dbName);
	  stmt = con->createStatement();

	  std::string strBuff;
	  char buffer[500];

	  sprintf(buffer, "delete from location;");
	  strBuff = buffer;

	  stmt->executeUpdate(strBuff);

	  	  delete stmt;
	  	  delete con;

 	   }catch (sql::SQLException &e) {
 		   cout << "# ERR: SQLException in " << __FILE__;
 		   cout << "# ERR: " << e.what();
 		   cout << " (MySQL error code: " << e.getErrorCode();
 		   cout << ", SQLState: " << e.getSQLState() << " )" << endl;
     }

}

double ToValveTime(int year, int month, int day, int hour, int minute, int second) {

    double epochDouble;

    struct tm t;
    time_t t_of_day;

    t.tm_year = year - 1900;
    t.tm_mon = month-1 ;       // Month, 0 - jan
    t.tm_mday = day;           // Day of the month
    t.tm_hour = hour;
    t.tm_min = minute;
    t.tm_sec = second;
    t.tm_isdst = -1;           // Is DST on? 1 = yes, 0 = no, -1 = unknown
    t_of_day = timegm(&t);

    epochDouble = (double)t_of_day;

    return epochDouble-946728000;
}

void ToRealTime(double epochTime, int &year, int &month, int &day) {
	long int c = (long int)epochTime;
	struct tm *date = gmtime( &c );

	year  = date->tm_year+1900;
	month = date->tm_mon+1;
	day   = date->tm_mday;

}

double addDay(int &year, int &month, int &day) {

    double epochDouble;

    struct tm t;
    time_t t_of_day;

    t.tm_year = year - 1900;
    t.tm_mon = month-1 ;       // Month, 0 - jan
    t.tm_mday = day;           // Day of the month
    t.tm_hour = 0;
    t.tm_min = 0;
    t.tm_sec = 0;
    t.tm_isdst = -1;           // Is DST on? 1 = yes, 0 = no, -1 = unknown
    t_of_day = timegm(&t);

    epochDouble = (double)t_of_day;

    epochDouble = epochDouble + 86400;

    ToRealTime(epochDouble, year, month, day);

    return epochDouble;
}

void readPicking(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int secondsOfData, double epochTime[], double amplitude[], int &count_data,  double startTime, double endTime){

 dbName.erase(remove(dbName.begin(), dbName.end(), '\\'), dbName.end());

 std::string strBuff;
 char buffer[500];


 if(month > 9 && day > 9)
    sprintf(buffer, "%d_%d_%d", year,month,day);
 else if(month <10 && day > 9)
    sprintf(buffer, "%d_0%d_%d", year,month,day);
 else if(month >9 && day < 10)
    sprintf(buffer, "%d_%d_0%d", year,month,day);
 else if(month <10 && day < 10)
    sprintf(buffer, "%d_0%d_0%d", year,month,day);

 strBuff = buffer;

 std::string tableName = dbName+"$$"+strBuff;
 dbName = "w_"+dbName;


 using namespace sql;

  try{
      sql::Driver *driver;
	  sql::Connection *con;
	  sql::Statement *stmt;
	  sql::ResultSet  *res;

	  // Create a connection
	  driver = get_driver_instance();
	  con = driver->connect(ipAddress, dbUser, dbPassword);

	  con->setSchema(dbName);
	  stmt = con->createStatement();

	  std::string strBuff;
	  char buffer[500];

	  sprintf(buffer, "select st,et,amplitude,millisecond from %s where (st<%lf and et>%lf) or (st>=%lf  and st<%lf) ORDER BY st ASC", tableName.c_str(), startTime,startTime,startTime,endTime);
	  strBuff = buffer;

	  res = stmt->executeQuery(strBuff);

	  while (res->next()) {
	    // You can use either numeric offsets...
		double st = res->getDouble(1) + 946728000;
		int milli = res->getInt(4);
		st = st + double(milli/1000.0);

		epochTime[count_data] = st;
		amplitude[count_data] = res->getDouble(3);
		count_data ++;
	    //cout << " millisecon" + ds = "<< setprecision(14) << st << "  --> " << res->getDouble(3) << endl; // getInt(1) returns the first column

	  }

	  delete res;
	  delete stmt;
	  delete con;

 	   }catch (sql::SQLException &e) {

     }


}


void readPicking(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int secondsOfData, double epochTime[], double amplitude[], int &size){

  size = 0;

  double startTime = ToValveTime(year, month, day, hour, minute, second);
  double endTime   = startTime + secondsOfData;

  readPicking(ipAddress, dbUser, dbPassword, dbName, year, month, day, hour, minute, second, secondsOfData, epochTime, amplitude, size,startTime,endTime);

  addDay(year,month,day);

  readPicking(ipAddress, dbUser, dbPassword, dbName, year, month, day, hour, minute, second, secondsOfData, epochTime, amplitude, size,startTime,endTime);

}





