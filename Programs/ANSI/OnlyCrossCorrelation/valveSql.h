
void readDataFromValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int secondsOfData, int** data, int &size , int &samplingRate);
void writeDataToValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int data[], int size, int samplingRate);
void removeDataBaseValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName);
void readStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, double &longitude, double &latitude, double &z, double &scaler);
void writePickingToValve(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int millisecond, float amplitude);
void writeEventLocation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int millisecond, float lng,float lat,float z,float magnitude);
void writeStationLocation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName, std::string stationName, float lng,float lat,float depth);
void removeStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName, std::string stationName);
void removeAllStation(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName);
void removeAllEvents(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string deploymentName);
void readPicking(std::string ipAddress, std::string dbUser, std::string dbPassword, std::string dbName, int year, int month, int day, int hour, int minute, int second, int secondsOfData, double epochTime[], double amplitude[], int &size);
