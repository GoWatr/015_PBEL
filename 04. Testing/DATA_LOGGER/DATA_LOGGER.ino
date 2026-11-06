#include <Arduino.h>
#include <SoftwareSerial.h>
#include <HTTPUpdate.h>
#define LED_BUILTIN 2
const byte num_slaveIDs = 15;
const byte num_bytes_in_frame = 8;
const byte num_bytes_to_read = 12;
int V8_BIT_1, V8_BIT_2;
uint64_t V16_BIT_1;

SoftwareSerial SerialRS485(26, 27); // rx,tx
const char *serverUrl = "https://www.ggggowatr.com/wms/pushdata/brownstone_data.php?project_id=browna&data=";

byte values[num_bytes_to_read];
String ID_srv = "Sump";
String ID_rawvalue = "rawvalue:";
String ID_percentage = ",percentage:";
String datasend = "";

int32_t TOT[num_slaveIDs];
int16_t FLOW[num_slaveIDs];

// Define request frames for each slave ID
const byte requestframes[num_slaveIDs][num_bytes_in_frame] = {
  {0x01, 0x03, 0x00, 0x00, 0x00, 0x04, 0x44, 0x09}, // Slave ID 1
  {0x02, 0x03, 0x00, 0x00, 0x00, 0x04, 0x44, 0x3A}, // Slave ID 2
  {0x03, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0xe4}, // Slave ID 3
  {0x04, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x53},
  {0x05, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0x82},
  {0x06, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0xB1},
  {0x07, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x60},
  {0x08, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0x9F},
  {0x09, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0x4E},
  {0x0A, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0x66},
  {0x0B, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0xAC},
  {0x0C, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0x1B},
  {0x0D, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0xCA},
  {0x0E, 0x03, 0x00, 0x00, 0x00, 0x10, 0x44, 0xF9},
  {0x0F, 0x03, 0x00, 0x00, 0x00, 0x10, 0x45, 0x28},
};

void setup() {
  Serial.begin(9600);
  SerialRS485.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  
  for (byte slaveID = 0; slaveID < num_slaveIDs; slaveID++) {
    byte requestframe[num_bytes_in_frame];
    memcpy(requestframe, requestframes[slaveID], num_bytes_in_frame);
    
    if (SerialRS485.write(requestframe, num_bytes_in_frame) == num_bytes_in_frame) 
    {
      delay(2000);
      /*delay(500);
      for (byte i = 0; i < num_bytes_to_read; i++)
      {
        values[i] = SerialRS485.read();
        delay(50);
      }
      Serial.print(ID_srv + String(slaveID + 1) + " Received BYTES: ");
      for (byte i = 0; i < num_bytes_to_read; i++)
      {
        Serial.print(values[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      //TOT[slaveID] = (values[3] << 24) | (values[4] << 16) | (values[5] << 8) | values[6];
      FLOW[slaveID] = (values[8] << 8) | values[9];
      V8_BIT_1 = (values[3] << 8) | values[4];
      V8_BIT_2 = (values[5] << 8) | values[6];
      
      TOT[slaveID] = static_cast<uint64_t>(V8_BIT_1) << 16 | V8_BIT_2;
      Serial.println("Totalizer is : " + String(TOT[slaveID]));
      Serial.println("Flowrate  is : " + String(FLOW[slaveID]));*/
    }
  }
  /*Serial.println("Tot: " + String(TOT[1]) + "Flow: " + String(FLOW[1]));
  Serial.println("Tot: " + String(TOT[2]) + "Flow: " + String(FLOW[2]));
  Serial.println("Tot: " + String(TOT[3]) + "Flow: " + String(FLOW[3]));
  Serial.println("Tot: " + String(TOT[4]) + "Flow: " + String(FLOW[4]));
  Serial.println("Tot: " + String(TOT[5]) + "Flow: " + String(FLOW[5]));
  Serial.println("Tot: " + String(TOT[6]) + "Flow: " + String(FLOW[6]));
  Serial.println("Tot: " + String(TOT[7]) + "Flow: " + String(FLOW[7]));
  Serial.println("Tot: " + String(TOT[8]) + "Flow: " + String(FLOW[8]));
  Serial.println("Tot: " + String(TOT[9]) + "Flow: " + String(FLOW[9]));
  Serial.println("Tot: " + String(TOT[10]) + "Flow: " + String(FLOW[10]));
  Serial.println("Tot: " + String(TOT[11]) + "Flow: " + String(FLOW[11]));
  Serial.println("Tot: " + String(TOT[12]) + "Flow: " + String(FLOW[12]));
  Serial.println("Tot: " + String(TOT[13]) + "Flow: " + String(FLOW[13]));
  Serial.println("Tot: " + String(TOT[14]) + "Flow: " + String(FLOW[14]));
  Serial.println("Tot: " + String(TOT[15]) + "Flow: " + String(FLOW[15]));*/
}
