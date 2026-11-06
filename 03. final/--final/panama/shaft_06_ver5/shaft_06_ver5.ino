//***************************************************************************
// PROJECT NAME: PBEL
// IC USED:ESP 32
// DEVELOPED BY: vasanth
// LAST UPDATE DATE:29/09/2024
// MODIFIED BY: jithendra
//board manager version : esp32 by espressif system 3.0.4
//***************************************************************************
#include <SoftwareSerial.h>
#include <Ticker.h>
#define LED 2
#define device_id 6
const byte ModReadBuffer1[] = { 83, 0x03, 0x00, 0x00, 0x00, 0x04, 0x45, 0x27 };
const byte ModReadBuffer2[] = { 84, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0x48 };
const byte ModReadBuffer3[] = { 85, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0x99 };
const byte ModReadBuffer4[] = { 86, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0xAA };
const byte ModReadBuffer5[] = { 87, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0x7B };
const byte ModReadBuffer6[] = { 88, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0xCC };
const byte ModReadBuffer7[] = { 89, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0x1D };
const byte ModReadBuffer8[] = { 90, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0x2E };
const byte ModReadBuffer9[] = { 91, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0xFF };
const byte ModReadBuffer10[] = { 92, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0x00 };
const byte ModReadBuffer11[] = { 93, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0xD1 };
const byte ModReadBuffer12[] = { 94, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0xE2 };
const byte ModReadBuffer13[] = { 95, 0x03, 0x00, 0x00, 0x00, 0x04, 0x46, 0x33 };
const byte ModReadBuffer14[] = { 96, 0x03, 0x00, 0x00, 0x00, 0x04, 0x47, 0x84 };
uint8_t BufferValue[8];
SoftwareSerial mod(26, 27);  // RX=26 , TX =27
SoftwareSerial mod1(16, 17);
byte fm1_byte[20], fm2_byte[20], fm3_byte[20], fm4_byte[20], fm5_byte[20], fm6_byte[20], fm7_byte[20];
byte fm8_byte[20], fm9_byte[20], fm10_byte[20], fm11_byte[20], fm12_byte[20], fm13_byte[20], fm14_byte[20];
byte dl1_byte[20];
uint8_t rx_buffer[20];
uint8_t tx_buffer[250];
Ticker secondTick;
uint8_t value;
volatile int watchdogCount = 0;
void ISRwatchdog() {
  watchdogCount++;
  datalogwrite();
  if (watchdogCount == 5) {
    Serial.println();
    Serial.println("the watchdog bites!!!!");
  }
}
uint16_t CalcCRC(const uint8_t* const buffer, const uint8_t u8length) {
  uint32_t temp;
  uint32_t temp2;
  uint32_t flag;
  temp = 0xFFFF;
  for (uint8_t i = 0; i < u8length; i++) {
    temp = temp ^ buffer[i];
    for (uint8_t j = 1; j <= 8; j++) {
      flag = temp & 0x0001;
      temp >>= 1;
      if (flag)
        temp ^= 0xA001;
    }
  }
  // Reverse byte order.
  temp2 = temp >> 8;
  temp = (temp << 8) | temp2;
  temp &= 0xFFFF;
  return (uint16_t)temp;
}

void setup() {
  pinMode(LED, OUTPUT);
  secondTick.attach(1, ISRwatchdog);
  Serial.begin(115200);
  mod.begin(9600);
  mod1.begin(9600);
}
void loop() {
  byte i;
  fm1_modbusread();
  delay(5000);
  fm2_modbusread();
  delay(5000);
  fm3_modbusread();
  delay(5000);
  fm4_modbusread();
  delay(5000);
  fm5_modbusread();
  delay(5000);
  fm6_modbusread();
  delay(5000);
  fm7_modbusread();
  delay(5000);
  fm8_modbusread();
  delay(5000);
  fm9_modbusread();
  delay(5000);
  fm10_modbusread();
  delay(5000);
  fm11_modbusread();
  delay(5000);
  fm12_modbusread();
  delay(5000);
  fm13_modbusread();
  delay(5000);
  fm14_modbusread();
  delay(5000);
}
void fm1_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer1, sizeof(ModReadBuffer1)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm1_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES1: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm1_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm1_byte[0] == ModReadBuffer1[0]) && (fm1_byte[1] == 3)) {  // Check point
        fm1_byte[0] = 1;
        uint32_t totalizer = (((uint32_t)fm1_byte[3] << 24) | ((uint32_t)fm1_byte[4] << 16) | ((uint32_t)fm1_byte[5] << 8) | fm1_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[3], &fm1_byte[0], 1);
        codetranfer(&tx_buffer[4], &fm1_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm1_byte[i] = 0;
        }
        codetranfer(&tx_buffer[3], &fm1_byte[0], 1);
        codetranfer(&tx_buffer[4], &fm1_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm2_modbusread() {
  bool condition_met = false;
  for (int attempt = 0; attempt < 3; attempt++) {
    // memset(fm2_byte, 0, sizeof(fm2_byte));
    if (mod.write(ModReadBuffer2, sizeof(ModReadBuffer2)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm2_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES2: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm2_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm2_byte[0] == ModReadBuffer2[0]) && (fm2_byte[1] == 3)) {  // Check point
        fm2_byte[0] = 2;
        uint32_t totalizer = (((uint32_t)fm2_byte[3] << 24) | ((uint32_t)fm2_byte[4] << 16) | ((uint32_t)fm2_byte[5] << 8) | fm2_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[11], &fm2_byte[0], 1);
        codetranfer(&tx_buffer[12], &fm2_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm2_byte[i] = 0;
        }
        codetranfer(&tx_buffer[11], &fm2_byte[0], 1);
        codetranfer(&tx_buffer[12], &fm2_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm3_modbusread() {
  bool condition_met = false;
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer3, sizeof(ModReadBuffer3)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm3_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES3: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm3_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm3_byte[0] == ModReadBuffer3[0]) && (fm3_byte[1] == 3)) {  // Check point
        fm3_byte[0] = 3;
        uint32_t totalizer = (((uint32_t)fm3_byte[3] << 24) | ((uint32_t)fm3_byte[4] << 16) | ((uint32_t)fm3_byte[5] << 8) | fm3_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[19], &fm3_byte[0], 1);
        codetranfer(&tx_buffer[20], &fm3_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm3_byte[i] = 0;
        }
        codetranfer(&tx_buffer[19], &fm3_byte[0], 1);
        codetranfer(&tx_buffer[20], &fm3_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm4_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer4, sizeof(ModReadBuffer4)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm4_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES4: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm4_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm4_byte[0] == ModReadBuffer4[0]) && (fm4_byte[1] == 3)) {  // Check point
        fm4_byte[0] = 4;
        uint32_t totalizer = (((uint32_t)fm4_byte[3] << 24) | ((uint32_t)fm4_byte[4] << 16) | ((uint32_t)fm4_byte[5] << 8) | fm4_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[27], &fm4_byte[0], 1);
        codetranfer(&tx_buffer[28], &fm4_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm4_byte[i] = 0;
        }
        codetranfer(&tx_buffer[27], &fm4_byte[0], 1);
        codetranfer(&tx_buffer[28], &fm4_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm5_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer5, sizeof(ModReadBuffer5)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm5_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES5: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm5_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm5_byte[0] == ModReadBuffer5[0]) && (fm5_byte[1] == 3)) {  // Check point
        fm5_byte[0] = 5;
        uint32_t totalizer = (((uint32_t)fm5_byte[3] << 24) | ((uint32_t)fm5_byte[4] << 16) | ((uint32_t)fm5_byte[5] << 8) | fm5_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[35], &fm5_byte[0], 1);
        codetranfer(&tx_buffer[36], &fm5_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm5_byte[i] = 0;
        }
        codetranfer(&tx_buffer[35], &fm5_byte[0], 1);
        codetranfer(&tx_buffer[36], &fm5_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm6_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer6, sizeof(ModReadBuffer6)) == 8) {
      mod.flush();
      delay(500);
      for (byte i = 0; i < 20; i++) {
        fm6_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES6: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm6_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm6_byte[0] == ModReadBuffer6[0]) && (fm6_byte[1] == 3)) {  // Check point
        fm6_byte[0] = 6;
        uint32_t totalizer = (((uint32_t)fm6_byte[3] << 24) | ((uint32_t)fm6_byte[4] << 16) | ((uint32_t)fm6_byte[5] << 8) | fm6_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[43], &fm6_byte[0], 1);
        codetranfer(&tx_buffer[44], &fm6_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm6_byte[i] = 0;
        }
        codetranfer(&tx_buffer[43], &fm6_byte[0], 1);
        codetranfer(&tx_buffer[44], &fm6_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm7_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer7, sizeof(ModReadBuffer7)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm7_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES7: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm7_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm7_byte[0] == ModReadBuffer7[0]) && (fm7_byte[1] == 3)) {  // Check point
        fm7_byte[0] = 7;
        uint32_t totalizer = (((uint32_t)fm7_byte[3] << 24) | ((uint32_t)fm7_byte[4] << 16) | ((uint32_t)fm7_byte[5] << 8) | fm7_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[51], &fm7_byte[0], 1);
        codetranfer(&tx_buffer[52], &fm7_byte[3], 7);
        condition_met = true;
        break;
      } else {
        fm7_byte[3] = 0;
        for (int i = 0; i < 20; i++) {
          fm7_byte[i] = 0;
        }
        codetranfer(&tx_buffer[51], &fm7_byte[0], 1);
        codetranfer(&tx_buffer[52], &fm7_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm8_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer8, sizeof(ModReadBuffer8)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm8_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES8: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm8_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm8_byte[0] == ModReadBuffer8[0]) && (fm8_byte[1] == 3)) {  // Check point
        fm8_byte[0] = 8;
        uint32_t totalizer = (((uint32_t)fm8_byte[3] << 24) | ((uint32_t)fm8_byte[4] << 16) | ((uint32_t)fm8_byte[5] << 8) | fm8_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[59], &fm8_byte[0], 1);
        codetranfer(&tx_buffer[60], &fm8_byte[3], 7);
        condition_met = true;
        break;
      }  else {
        for (int i = 0; i < 20; i++) {
          fm8_byte[i] = 0;
        }
        codetranfer(&tx_buffer[59], &fm8_byte[0], 1);
        codetranfer(&tx_buffer[60], &fm8_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm9_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer9, sizeof(ModReadBuffer9)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm9_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES9: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm9_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm9_byte[0] == ModReadBuffer9[0]) && (fm9_byte[1] == 3)) {  // Check point
        fm9_byte[0] = 9;
        uint32_t totalizer = (((uint32_t)fm9_byte[3] << 24) | ((uint32_t)fm9_byte[4] << 16) | ((uint32_t)fm9_byte[5] << 8) | fm9_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[67], &fm9_byte[0], 1);
        codetranfer(&tx_buffer[68], &fm9_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm9_byte[i] = 0;
        }
        codetranfer(&tx_buffer[67], &fm9_byte[0], 1);
        codetranfer(&tx_buffer[68], &fm9_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm10_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer10, sizeof(ModReadBuffer10)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm10_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES10: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm10_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm10_byte[0] == ModReadBuffer10[0]) && (fm10_byte[1] == 3)) {  // Check point
        fm10_byte[0] = 10;
        uint32_t totalizer = (((uint32_t)fm10_byte[3] << 24) | ((uint32_t)fm10_byte[4] << 16) | ((uint32_t)fm10_byte[5] << 8) | fm10_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[75], &fm10_byte[0], 1);
        codetranfer(&tx_buffer[76], &fm10_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm10_byte[i] = 0;
        }
        codetranfer(&tx_buffer[75], &fm10_byte[0], 1);
        codetranfer(&tx_buffer[76], &fm10_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm11_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer11, sizeof(ModReadBuffer11)) == 8) {
      mod.flush();
      delay(1000);

      for (byte i = 0; i < 20; i++) {
        fm11_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES11: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm11_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm11_byte[0] == ModReadBuffer11[0]) && (fm11_byte[1] == 3)) {  // Check point
        fm11_byte[0] = 11;
        uint32_t totalizer = (((uint32_t)fm11_byte[3] << 24) | ((uint32_t)fm11_byte[4] << 16) | ((uint32_t)fm11_byte[5] << 8) | fm11_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[83], &fm11_byte[0], 1);
        codetranfer(&tx_buffer[84], &fm11_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm11_byte[i] = 0;
        }
        codetranfer(&tx_buffer[83], &fm11_byte[0], 1);
        codetranfer(&tx_buffer[84], &fm11_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm12_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer12, sizeof(ModReadBuffer12)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm12_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES12: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm12_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm12_byte[0] == ModReadBuffer12[0]) && (fm12_byte[1] == 3)) {  // Check point
        fm12_byte[0] = 12;
        uint32_t totalizer = (((uint32_t)fm12_byte[3] << 24) | ((uint32_t)fm12_byte[4] << 16) | ((uint32_t)fm12_byte[5] << 8) | fm12_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[91], &fm12_byte[0], 1);
        codetranfer(&tx_buffer[92], &fm12_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm12_byte[i] = 0;
        }
        codetranfer(&tx_buffer[91], &fm12_byte[0], 1);
        codetranfer(&tx_buffer[92], &fm12_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm13_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer13, sizeof(ModReadBuffer13)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm13_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES13: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm13_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm13_byte[0] == ModReadBuffer13[0]) && (fm13_byte[1] == 3)) {  // Check point
        fm13_byte[0] = 13;
        uint32_t totalizer = (((uint32_t)fm13_byte[3] << 24) | ((uint32_t)fm13_byte[4] << 16) | ((uint32_t)fm13_byte[5] << 8) | fm13_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[99], &fm13_byte[0], 1);
        codetranfer(&tx_buffer[100], &fm13_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm13_byte[i] = 0;
        }
        codetranfer(&tx_buffer[99], &fm13_byte[0], 1);
        codetranfer(&tx_buffer[100], &fm13_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}
void fm14_modbusread() {
  bool condition_met = false;  // Flag to track if condition is met
  for (int attempt = 0; attempt < 3; attempt++) {
    if (mod.write(ModReadBuffer14, sizeof(ModReadBuffer14)) == 8) {
      mod.flush();
      delay(1000);
      for (byte i = 0; i < 20; i++) {
        fm14_byte[i] = mod.read();
        delay(50);
      }
      Serial.print("Received BYTES14: ");
      for (byte i = 0; i < 20; i++) {
        Serial.print(fm14_byte[i], HEX);
        Serial.print(' ');
      }
      Serial.println(" ");
      if ((fm14_byte[0] == ModReadBuffer14[0]) && (fm14_byte[1] == 3)) {  // Check point
        fm14_byte[0] = 14;
        uint32_t totalizer = (((uint32_t)fm14_byte[3] << 24) | ((uint32_t)fm14_byte[4] << 16) | ((uint32_t)fm14_byte[5] << 8) | fm14_byte[6]);
        Serial.println("Totalizer: " + String(totalizer));
        codetranfer(&tx_buffer[107], &fm14_byte[0], 1);
        codetranfer(&tx_buffer[108], &fm14_byte[3], 7);
        condition_met = true;
        break;
      } else {
        for (int i = 0; i < 20; i++) {
          fm14_byte[i] = 0;
        }
        codetranfer(&tx_buffer[107], &fm14_byte[0], 1);
        codetranfer(&tx_buffer[108], &fm14_byte[3], 7);
      }
      if (condition_met)
        break;
    }
  }
}

void datalogwrite() {
  if (mod1.available() > 0) {
    for (byte i = 0; i < 8; i++) {
      rx_buffer[i] = mod1.read();
    }

    Serial.print("Data Logger Received BYTES: ");
    for (byte i = 0; i < 8; i++) {
      Serial.print(rx_buffer[i], HEX);
      Serial.print(' ');
      mod1.flush();
    }
    Serial.println(" ");

    if ((rx_buffer[0] == device_id) && (rx_buffer[1] == 3)) {
      Serial.println("write register");
      send_data();
    } else {
      Serial.println("condition not matched");
    }
  }
}

void send_data() {
  tx_buffer[0] = rx_buffer[0];
  tx_buffer[1] = rx_buffer[1];
  tx_buffer[2] = (rx_buffer[5] * 2);

  // Calculate CRC for data integrity
  uint8_t size = ((rx_buffer[5] * 2) + 3);
  uint16_t u16crc = CalcCRC(tx_buffer, size);
  uint8_t xlow = u16crc & 0xff;
  uint8_t xhigh = (u16crc >> 8);

  tx_buffer[size + 1] = xlow;
  tx_buffer[size] = xhigh;

  Serial.println("Data Logger write BYTES: ");
  Serial.println(String(u16crc));
  Serial.println(tx_buffer[size + 1]);
  Serial.println(tx_buffer[size]);
  Serial.println(String(size));

  for (byte i = 0; i <= size + 1; i++) {
    Serial.print(tx_buffer[i], HEX);
    Serial.print(' ');
    mod1.flush();
  }
  Serial.println(" ");
  mod1.write(tx_buffer, sizeof(tx_buffer));
  delay(200);
  // mod1.write(tx_buffer, size + 2);  // Send the data
}
void codetranfer(uint8_t* dstpntr, uint8_t* srcpntr, uint8_t counter) {
  int cnt;
  for (cnt = 0; cnt < counter; cnt++) {
    *dstpntr = *srcpntr;
    dstpntr++;
    srcpntr++;
  }
}