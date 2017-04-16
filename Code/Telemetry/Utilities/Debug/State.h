/* 
A data storage class
*/
class State{ 
private:

unsigned int gpsTime;
unsigned int latitude;
unsigned int longitude;
unsigned int altitude;
unsigned int speed;
unsigned int angle;
unsigned int accelerationX;
unsigned int accelerationY;
unsigned int accelerationZ;
unsigned int gyroX;
unsigned int gyroY;
unsigned int gyroZ;
unsigned int compassX;
unsigned int compassY;
unsigned int compassZ;
unsigned int tempFrontIMU;
unsigned int tempFrontDiscrete;
unsigned int brakePressureFront;
unsigned int brakePressureRear;
unsigned int temperatureCVT;
/* 
Not sure how useful this is…
*/
unsigned int temperatureRegulatorBoard;
unsigned int temperatureGearbox;
unsigned int steeringPosition;
unsigned int rpmFrontRight;
unsigned int rpmFrontLeft;
unsigned int rpmRearRight;
unsigned int rpmRearLeft;
unsigned int rpmPrimary;
unsigned int rpmSecondary;
bool tieRodLeft;
bool tieRodRight;

public:

// Get the value of gpsTime
unsigned int getGpsTime();
// Set the value of gpsTime
void setGpsTime(unsigned int gpsTime);

// Get the value of latitude
unsigned int getLatitude();
// Set the value of latitude
void setLatitude(unsigned int latitude);

// Get the value of longitude
unsigned int getLongitude();
// Set the value of longitude
void setLongitude(unsigned int longitude);

// Get the value of altitude
unsigned int getAltitude();
// Set the value of altitude
void setAltitude(unsigned int altitude);

// Get the value of speed
unsigned int getSpeed();
// Set the value of speed
void setSpeed(unsigned int speed);

// Get the value of angle
unsigned int getAngle();
// Set the value of angle
void setAngle(unsigned int angle);

// Get the value of accelerationX
unsigned int getAccelerationX();
// Set the value of accelerationX
void setAccelerationX(unsigned int accelerationX);

// Get the value of accelerationY
unsigned int getAccelerationY();
// Set the value of accelerationY
void setAccelerationY(unsigned int accelerationY);

// Get the value of accelerationZ
unsigned int getAccelerationZ();
// Set the value of accelerationZ
void setAccelerationZ(unsigned int accelerationZ);

// Get the value of gyroX
unsigned int getGyroX();
// Set the value of gyroX
void setGyroX(unsigned int gyroX);

// Get the value of gyroY
unsigned int getGyroY();
// Set the value of gyroY
void setGyroY(unsigned int gyroY);

// Get the value of gyroZ
unsigned int getGyroZ();
// Set the value of gyroZ
void setGyroZ(unsigned int gyroZ);

// Get the value of compassX
unsigned int getCompassX();
// Set the value of compassX
void setCompassX(unsigned int compassX);

// Get the value of compassY
unsigned int getCompassY();
// Set the value of compassY
void setCompassY(unsigned int compassY);

// Get the value of compassZ
unsigned int getCompassZ();
// Set the value of compassZ
void setCompassZ(unsigned int compassZ);

// Get the value of tempFrontIMU
unsigned int getTempFrontIMU();
// Set the value of tempFrontIMU
void setTempFrontIMU(unsigned int tempFrontIMU);

// Get the value of tempFrontDiscrete
unsigned int getTempFrontDiscrete();
// Set the value of tempFrontDiscrete
void setTempFrontDiscrete(unsigned int tempFrontDiscrete);

// Get the value of brakePressureFront
unsigned int getBrakePressureFront();
// Set the value of brakePressureFront
void setBrakePressureFront(unsigned int brakePressureFront);

// Get the value of brakePressureRear
unsigned int getBrakePressureRear();
// Set the value of brakePressureRear
void setBrakePressureRear(unsigned int brakePressureRear);

// Get the value of temperatureCVT
unsigned int getTemperatureCVT();
// Set the value of temperatureCVT
void setTemperatureCVT(unsigned int temperatureCVT);

// Get the value of temperatureRegulatorBoard
unsigned int getTemperatureRegulatorBoard();
// Set the value of temperatureRegulatorBoard
void setTemperatureRegulatorBoard(unsigned int temperatureRegulatorBoard);

// Get the value of temperatureGearbox
unsigned int getTemperatureGearbox();
// Set the value of temperatureGearbox
void setTemperatureGearbox(unsigned int temperatureGearbox);

// Get the value of steeringPosition
unsigned int getSteeringPosition();
// Set the value of steeringPosition
void setSteeringPosition(unsigned int steeringPosition);

// Get the value of rpmFrontRight
unsigned int getRpmFrontRight();
// Set the value of rpmFrontRight
void setRpmFrontRight(unsigned int rpmFrontRight);

// Get the value of rpmFrontLeft
unsigned int getRpmFrontLeft();
// Set the value of rpmFrontLeft
void setRpmFrontLeft(unsigned int rpmFrontLeft);

// Get the value of rpmRearRight
unsigned int getRpmRearRight();
// Set the value of rpmRearRight
void setRpmRearRight(unsigned int rpmRearRight);

// Get the value of rpmRearLeft
unsigned int getRpmRearLeft();
// Set the value of rpmRearLeft
void setRpmRearLeft(unsigned int rpmRearLeft);

// Get the value of rpmPrimary
unsigned int getRpmPrimary();
// Set the value of rpmPrimary
void setRpmPrimary(unsigned int rpmPrimary);

// Get the value of rpmSecondary
unsigned int getRpmSecondary();
// Set the value of rpmSecondary
void setRpmSecondary(unsigned int rpmSecondary);

// Get the value of tieRodLeft
bool getTieRodLeft();
// Set the value of tieRodLeft
void setTieRodLeft(bool tieRodLeft);

// Get the value of tieRodRight
bool getTieRodRight();
// Set the value of tieRodRight
void setTieRodRight(bool tieRodRight);


}