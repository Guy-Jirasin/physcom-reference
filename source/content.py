"""Course content and complete UNO R4 sketches. All generated code is editable."""
import json
from pathlib import Path

SKETCHES={}
def sketch(key,code):
    SKETCHES[key]=code.strip()+'\n'
    return key

sketch('ultrasonic',r'''
const byte TRIG = 4;
const byte ECHO = 2;
void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}
void loop() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long us = pulseIn(ECHO, HIGH, 25000UL);
  if (us == 0) {
    Serial.println("No echo");
  } else {
    float cm = us * 0.0343f / 2.0f;
    Serial.print(cm, 2);
    Serial.println(" cm");
  }
  delay(100);
}
''')
sketch('mcp9700',r'''
// MCP9700: 500 mV at 0 C, slope 10 mV/C.
const byte TEMP_PIN = A0;
const float VREF = 5.0f; // Change to measured reference if needed.
void setup() {
  Serial.begin(9600);
  analogReadResolution(10);
}
void loop() {
  int raw = analogRead(TEMP_PIN);
  float voltage = raw * VREF / 1023.0f;
  float tempC = (voltage - 0.5f) * 100.0f;
  Serial.print(tempC, 2);
  Serial.println(" C");
  delay(250);
}
''')
sketch('thermistor',r'''
#include <math.h>
// 5V -> fixed 10k -> A0 -> NTC -> GND (do not swap).
const float R_FIXED = 10000.0f;
const float R0 = 10000.0f;
const float T0 = 298.15f; // 25 C in kelvin
const float BETA = 4050.0f; // TTC05103, B25/50 per course
void setup() {
  Serial.begin(9600);
  analogReadResolution(10);
}
void loop() {
  int raw = analogRead(A0);
  if (raw <= 0 || raw >= 1023) {
    Serial.println("Check NTC wiring");
  } else {
    float r = R_FIXED * raw / (1023.0f - raw);
    float k = 1.0f / (1.0f/T0 + log(r/R0)/BETA);
    Serial.print(k - 273.15f, 2);
    Serial.println(" C");
  }
  delay(250);
}
''')
sketch('ldr',r'''
// 5V -> LDR -> A0 -> fixed 10k -> GND.
const int THRESHOLD = 500; // Calibrate using Serial Monitor.
void setup() {
  Serial.begin(9600);
  analogReadResolution(10);
  pinMode(4, OUTPUT);
}
void loop() {
  int raw = analogRead(A0);
  Serial.println(raw);
  digitalWrite(4, raw < THRESHOLD ? HIGH : LOW);
  delay(100);
}
''')
sketch('pot_pwm',r'''
void setup() {
  Serial.begin(9600);
  analogReadResolution(10);
  analogWriteResolution(8);
  pinMode(9, OUTPUT);
}
void loop() {
  int raw = analogRead(A0);
  int pwm = map(raw, 0, 1023, 0, 255);
  analogWrite(9, pwm);
  Serial.print(raw);
  Serial.print(" -> ");
  Serial.println(pwm);
  delay(50);
}
''')
sketch('led_blink',r'''
const byte LED = 9;
void setup() { pinMode(LED, OUTPUT); }
void loop() {
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500); // 500 + 500 ms = 1 Hz
}
''')
sketch('button',r'''
const byte BUTTON = 4;
const byte LED = 9;
void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
}
void loop() {
  bool pressed = digitalRead(BUTTON) == LOW;
  digitalWrite(LED, pressed ? HIGH : LOW);
}
''')
sketch('debounce',r'''
const byte BUTTON=4, LED=9;
bool lastRaw=HIGH, stable=HIGH, on=false;
unsigned long changedAt=0;
void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
}
void loop() {
  bool raw=digitalRead(BUTTON);
  if (raw!=lastRaw) { changedAt=millis(); lastRaw=raw; }
  if (millis()-changedAt>=30 && raw!=stable) {
    stable=raw;
    if (stable==LOW) { // One event on press, not while held
      on=!on;
      digitalWrite(LED,on);
    }
  }
}
''')
RGB=r'''
const byte RED=3, GREEN=5, BLUE=6;
void rgb(byte r, byte g, byte b) {
  // Common ANODE: 0 = fully on, 255 = off.
  analogWrite(RED,255-r);
  analogWrite(GREEN,255-g);
  analogWrite(BLUE,255-b);
}
void setupRGB() {
  pinMode(RED,OUTPUT); pinMode(GREEN,OUTPUT);
  pinMode(BLUE,OUTPUT); analogWriteResolution(8);
  rgb(0,0,0);
}
'''
sketch('rgb_colors',RGB+r'''
const byte colors[7][3]={
  {255,0,0},{0,255,0},{0,0,255},{255,255,0},
  {255,0,255},{0,255,255},{255,255,255}
};
void setup() { setupRGB(); }
void loop() {
  for (byte i=0;i<7;i++) {
    rgb(colors[i][0],colors[i][1],colors[i][2]);
    delay(1000);
  }
}
''')
sketch('pir',RGB+r'''
const byte PIR=4;
void setup() { setupRGB(); pinMode(PIR,INPUT); }
void loop() {
  if (digitalRead(PIR)==HIGH) rgb(0,255,0);
  else rgb(255,0,0);
}
''')
sketch('digital_module',r'''
// Digital OUT of the example IR / sound module is active LOW.
const byte SENSOR=4, LED=9;
void setup() {
  Serial.begin(9600);
  pinMode(SENSOR,INPUT);
  pinMode(LED,OUTPUT);
}
void loop() {
  bool detected=digitalRead(SENSOR)==LOW;
  digitalWrite(LED,detected);
  Serial.println(detected ? "Detected" : "Idle");
  delay(50);
}
''')
sketch('fading4',r'''
const byte pins[4]={3,5,6,9};
unsigned long started;
int triangle(unsigned long t,unsigned long period) {
  unsigned long phase=t%period;
  unsigned long half=period/2;
  if (phase<half) return map(phase,0,half,0,255);
  return map(phase,half,period,255,0);
}
void setup() {
  analogWriteResolution(8);
  for (byte p:pins) pinMode(p,OUTPUT);
  started=millis();
}
void loop() {
  unsigned long t=millis()-started;
  analogWrite(pins[0],triangle(t,4000));
  analogWrite(pins[1],triangle(t,2000)); // 2x faster
  analogWrite(pins[2],255-triangle(t,4000));
  analogWrite(pins[3],128+triangle(t,4000)*127/255);
}
''')
KEYPAD=r'''
const byte rows[4]={6,7,8,9};
const byte cols[4]={2,3,4,5};
const char keys[4][4]={
  {'1','2','3','A'}, {'4','5','6','B'},
  {'7','8','9','C'}, {'*','0','#','D'}
};
void setupKeypad() {
  for (byte p:rows) pinMode(p,INPUT_PULLUP);
  for (byte p:cols) pinMode(p,INPUT); // Inactive = high impedance
}
char scanKey() {
  char key=0;
  for (byte c=0;c<4;c++) {
    digitalWrite(cols[c],LOW);
    pinMode(cols[c],OUTPUT);
    delayMicroseconds(5);
    for (byte r=0;r<4;r++)
      if (digitalRead(rows[r])==LOW) key=keys[r][c];
    pinMode(cols[c],INPUT);
  }
  return key;
}
char keyPressed() {
  static char lastRaw=0,stable=0;
  static unsigned long changedAt=0;
  char raw=scanKey();
  if (raw!=lastRaw) { lastRaw=raw; changedAt=millis(); }
  if (millis()-changedAt>=30 && raw!=stable) {
    stable=raw;
    if (stable) return stable;
  }
  return 0;
}
'''
sketch('keypad',KEYPAD+r'''
void setup() { Serial.begin(9600); setupKeypad(); }
void loop() { char k=keyPressed(); if(k) Serial.println(k); }
''')
SEGMENTS=r'''
const byte segments[7]={2,3,4,5,6,7,8}; // a,b,c,d,e,f,g
const byte digits[10][7]={
 {1,1,1,1,1,1,0}, {0,1,1,0,0,0,0},
 {1,1,0,1,1,0,1}, {1,1,1,1,0,0,1},
 {0,1,1,0,0,1,1}, {1,0,1,1,0,1,1},
 {1,0,1,1,1,1,1}, {1,1,1,0,0,0,0},
 {1,1,1,1,1,1,1}, {1,1,1,1,0,1,1}
};
void setupSegments() { for(byte p:segments) pinMode(p,OUTPUT); }
void showDigit(byte n) {
  for(byte i=0;i<7;i++) digitalWrite(segments[i],digits[n][i]);
}
'''
sketch('seven_one',SEGMENTS+r'''
void setup() { setupSegments(); }
void loop() { for(byte i=0;i<10;i++){ showDigit(i);delay(1000); } }
''')
sketch('seven_two',SEGMENTS+r'''
// Common cathodes via NPN transistors; base resistor 1k each.
const byte enable[2]={10,11};
const byte idPairs[4]={68,7,0,12}; // CHANGE student ID pairs
void setup() {
  setupSegments();
  for(byte p:enable){ pinMode(p,OUTPUT);digitalWrite(p,LOW); }
}
void loop() {
  static unsigned long lastScan=0;
  static byte side=0;
  if(millis()-lastScan>=2) {
    lastScan=millis();
    digitalWrite(enable[0],LOW);
    digitalWrite(enable[1],LOW);
    byte value=idPairs[(millis()/1000)%4];
    showDigit(side==0 ? value/10 : value%10);
    digitalWrite(enable[side],HIGH);
    side=1-side;
  }
}
''')
sketch('seven_two_direct',r'''
// User-supplied direct common-cathode wiring (no NPN).
// LOW enables a digit; HIGH disables it. Do not use NPN wiring with this code.
// Check total common-pin current against the board's GPIO rating.
const byte num_array[10][7]={
 {1,1,1,1,1,1,0},{0,1,1,0,0,0,0},{1,1,0,1,1,0,1},
 {1,1,1,1,0,0,1},{0,1,1,0,0,1,1},{1,0,1,1,0,1,1},
 {1,0,1,1,1,1,1},{1,1,1,0,0,0,0},{1,1,1,1,1,1,1},
 {1,1,1,1,0,1,1}
};
const byte segmentPins[7]={4,5,8,6,7,3,2}; // a,b,c,d,e,f,g
const byte pinDP=9,pinDis1=10,pinDis2=11;
const char studentNum[]="68070015"; // Replace with your own even-length ID.
void displayDigit(int digit) {
 for(byte i=0;i<7;i++) digitalWrite(segmentPins[i],num_array[digit][i]);
}
void display2Digits(int first_digit,int second_digit,int duration_ms) {
 const int change_interval=5;
 int cycles=duration_ms/(change_interval*2);
 for(int i=0;i<cycles;i++) {
  digitalWrite(pinDis1,HIGH);digitalWrite(pinDis2,HIGH);
  displayDigit(first_digit);digitalWrite(pinDis1,LOW);delay(change_interval);
  digitalWrite(pinDis1,HIGH);digitalWrite(pinDis2,HIGH);
  displayDigit(second_digit);digitalWrite(pinDis2,LOW);delay(change_interval);
 }
 digitalWrite(pinDis1,HIGH);digitalWrite(pinDis2,HIGH);
}
void setup() {
 // Set output latch HIGH before enabling the common pins.
 digitalWrite(pinDis1,HIGH);digitalWrite(pinDis2,HIGH);
 pinMode(pinDis1,OUTPUT);pinMode(pinDis2,OUTPUT);
 for(byte p:segmentPins) pinMode(p,OUTPUT);
 pinMode(pinDP,OUTPUT);digitalWrite(pinDP,LOW);
}
void loop() {
 for(unsigned int i=0;i+1<sizeof(studentNum)-1;i+=2)
  display2Digits(studentNum[i]-'0',studentNum[i+1]-'0',500);
}
''')
keySeg=KEYPAD.replace('{6,7,8,9}','{A0,A1,A2,A3}')
segKey=SEGMENTS.replace('{2,3,4,5,6,7,8}','{6,7,8,9,10,11,12}')
sketch('keypad_seven',keySeg+segKey+r'''
void setup() { setupKeypad();setupSegments();showDigit(0); }
void loop() {
  char k=keyPressed();
  if(k>='0' && k<='9') showDigit(k-'0');
}
''')
LCD=r'''
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); // CHANGE using I2C scanner
'''
sketch('lcd_hello',LCD+r'''
void setup() {
  lcd.init(); lcd.backlight();
  lcd.print("hello, world!");
}
void loop() {
  static unsigned long last=0;
  if(millis()-last>=1000) {
    last=millis();lcd.setCursor(0,1);
    lcd.print("                ");lcd.setCursor(0,1);
    lcd.print(millis()/1000);
  }
}
''')
sketch('i2c_scanner',r'''
#include <Wire.h>
void setup() { Serial.begin(9600);Wire.begin(); }
void loop() {
  for(byte address=1;address<127;address++) {
    Wire.beginTransmission(address);
    if(Wire.endTransmission()==0) {
      Serial.print("I2C device: 0x");
      if(address<16) Serial.print('0');
      Serial.println(address,HEX);
    }
  }
  delay(3000);
}
''')
sketch('temp_lcd',LCD+r'''
void setup() {
  analogReadResolution(10);
  lcd.init();lcd.backlight();
}
void loop() {
  float voltage=analogRead(A0)*5.0f/1023.0f;
  float temp=(voltage-0.5f)*100.0f;
  lcd.setCursor(0,0);lcd.print("Temp:           ");
  lcd.setCursor(6,0);lcd.print(temp,2);lcd.print(" C");
  delay(250);
}
''')
sketch('lcd_custom',LCD+r'''
byte heart[8]={0,10,31,31,14,4,0,0};
byte degree[8]={6,9,9,6,0,0,0,0};
void setup() {
  analogReadResolution(10);
  lcd.init();lcd.backlight();
  lcd.createChar(0,heart);lcd.createChar(1,degree);
  lcd.setCursor(5,0);lcd.print("I ");
  lcd.write(byte(0));lcd.print(" IT");
}
void loop() {
  float temp=(analogRead(A0)*5.0f/1023.0f-0.5f)*100.0f;
  lcd.setCursor(0,1);lcd.print("68070012        "); // CHANGE ID
  lcd.setCursor(9,1);lcd.print(temp,2);lcd.write(byte(1));
  delay(500);
}
''')

def mqtt_sketch(key,client='tx',extras='',setup='',loop='',callback='',subscribe=False):
    header=r'''
#include <WiFiS3.h>
#include <MQTT.h>
// CHANGE these values before upload.
const char WIFI_SSID[]="YOUR_WIFI";
const char WIFI_PASS[]="YOUR_PASSWORD";
const char BROKER[]="mqtt-dashboard.com";
const int PORT=1883;
const char TOPIC[]="physcom/YOUR_ID/brightness";
'''+f'const char CLIENT_ID[]="YOUR_ID-{client}";\n'+r'''
WiFiClient net;
MQTTClient mqtt(256);
unsigned long lastWifiTry=0,lastMqttTry=0,lastSend=0;
bool triedWifi=false,triedMqtt=false;
'''+extras+'\n'+callback+r'''
void maintainConnection() {
  unsigned long now=millis();
  if(WiFi.status()!=WL_CONNECTED) {
    if(mqtt.connected()) mqtt.disconnect();
    if(!triedWifi || now-lastWifiTry>=10000UL) {
      triedWifi=true;lastWifiTry=now;
      Serial.println("WiFi connecting...");
      WiFi.begin(WIFI_SSID,WIFI_PASS);
    }
    return;
  }
  if(!mqtt.connected() && (!triedMqtt || now-lastMqttTry>=3000UL)) {
    triedMqtt=true;lastMqttTry=now;
    if(mqtt.connect(CLIENT_ID)) {
      Serial.println("MQTT connected");
'''+('      mqtt.subscribe(TOPIC,0); // Repeat after every reconnect\n' if subscribe else '')+r'''
    } else {
      Serial.print("MQTT error: ");Serial.println(mqtt.lastError());
    }
  }
}
void setup() {
  Serial.begin(9600);
'''+setup+r'''
  mqtt.begin(BROKER,PORT,net);
'''+('  mqtt.onMessage(messageReceived);\n' if callback else '')+r'''
}
void loop() {
  maintainConnection();
  mqtt.loop(); // Call frequently; do not add long delay here.
'''+loop+'\n}\n'
    return sketch(key,header)

mqtt_sketch('mqtt_base',subscribe=True,callback=r'''
void messageReceived(String &topic,String &payload) {
  Serial.println(topic+" : "+payload);
  // Do not publish/subscribe inside this callback.
}
''',loop=r'''
  if(mqtt.connected() && millis()-lastSend>=1000) {
    lastSend=millis();
    mqtt.publish("physcom/YOUR_ID/status",String(millis()/1000));
  }
''')
mqtt_sketch('mqtt_pot_tx',setup='  analogReadResolution(10);\n',loop=r'''
  if(mqtt.connected() && millis()-lastSend>=200) {
    lastSend=millis();
    int pwm=map(analogRead(A0),0,1023,0,255);
    mqtt.publish(TOPIC,String(pwm));
    Serial.println(pwm);
  }
''')
validate=r'''
bool validPWM(const String &s) {
  if(s.length()==0 || s.length()>3) return false;
  for(unsigned int i=0;i<s.length();i++)
    if(s[i]<'0' || s[i]>'9') return false;
  return s.toInt()<=255;
}
'''
mqtt_sketch('mqtt_pwm_rx',client='rx',extras=validate,setup='  pinMode(9,OUTPUT);analogWriteResolution(8);\n',subscribe=True,callback=r'''
void messageReceived(String &topic,String &payload) {
  if(topic==TOPIC && validPWM(payload)) {
    analogWrite(9,payload.toInt());
    Serial.println(payload);
  }
}
''')
mqtt_sketch('mqtt_keypad_tx',extras=KEYPAD,setup='  setupKeypad();\n',loop=r'''
  char k=keyPressed();
  if(k && mqtt.connected()) mqtt.publish(TOPIC,String(k));
''')
SKETCHES['mqtt_keypad_tx']=SKETCHES['mqtt_keypad_tx'].replace('/brightness','/key')
mqtt_sketch('mqtt_lcd_rx',client='rx',extras=LCD,setup='  lcd.init();lcd.backlight();lcd.print("Waiting MQTT");\n',subscribe=True,callback=r'''
void messageReceived(String &topic,String &payload) {
  if(topic!=TOPIC) return;
  lcd.setCursor(0,0);lcd.print("Key:            ");
  lcd.setCursor(5,0);lcd.print(payload.substring(0,11));
}
''')
SKETCHES['mqtt_lcd_rx']=SKETCHES['mqtt_lcd_rx'].replace('/brightness','/key')
mqtt_sketch('mqtt_temp_tx',setup='  analogReadResolution(10);\n',loop=r'''
  if(mqtt.connected() && millis()-lastSend>=1000) {
    lastSend=millis();
    float temp=(analogRead(A0)*5.0f/1023.0f-0.5f)*100.0f;
    mqtt.publish(TOPIC,String(temp,2));
  }
''')
SKETCHES['mqtt_temp_tx']=SKETCHES['mqtt_temp_tx'].replace('/brightness','/temperature')
mqtt_sketch('mqtt_temp_lcd_rx',client='rx',extras=LCD,setup='  lcd.init();lcd.backlight();\n',subscribe=True,callback=r'''
void messageReceived(String &topic,String &payload) {
  if(topic!=TOPIC) return;
  float temp=payload.toFloat(); // Expected trusted numeric temperature
  lcd.setCursor(0,0);lcd.print("Temp:           ");
  lcd.setCursor(6,0);lcd.print(temp,2);lcd.print(" C");
}
''')
SKETCHES['mqtt_temp_lcd_rx']=SKETCHES['mqtt_temp_lcd_rx'].replace('/brightness','/temperature')
mqtt_sketch('mqtt_temp_rgb_rx',client='rx',extras=RGB,setup='  setupRGB();\n',subscribe=True,callback=r'''
void messageReceived(String &topic,String &payload) {
  if(topic!=TOPIC) return;
  if(payload.toFloat()>=30.0f) rgb(255,0,0);
  else rgb(0,255,0);
}
''')
SKETCHES['mqtt_temp_rgb_rx']=SKETCHES['mqtt_temp_rgb_rx'].replace('/brightness','/temperature')
mqtt_sketch('mqtt_rgb_rx',client='rgb',extras=RGB+validate,setup='  setupRGB();\n',subscribe=True,callback=r'''
byte r=0,g=0,b=0;
void messageReceived(String &topic,String &payload) {
  if(!validPWM(payload)) return;
  if(topic=="physcom/YOUR_ID/rgb/r") r=payload.toInt();
  else if(topic=="physcom/YOUR_ID/rgb/g") g=payload.toInt();
  else if(topic=="physcom/YOUR_ID/rgb/b") b=payload.toInt();
  else return;
  rgb(r,g,b);
}
''')
SKETCHES['mqtt_rgb_rx']=SKETCHES['mqtt_rgb_rx'].replace('mqtt.subscribe(TOPIC,0);','mqtt.subscribe("physcom/YOUR_ID/rgb/+",0);')
SKETCHES['mqtt_rgb_rx']=SKETCHES['mqtt_rgb_rx'].replace('/brightness','/rgb')
mqtt_sketch('mqtt_switch_tx',setup='  for(byte p=4;p<=6;p++) pinMode(p,INPUT_PULLUP);\n',loop=r'''
  if(mqtt.connected() && millis()-lastSend>=200) {
    lastSend=millis();
    const char* names[3]={"r","g","b"};
    for(byte i=0;i<3;i++) {
      String topic=String("physcom/YOUR_ID/rgb/")+names[i];
      mqtt.publish(topic,digitalRead(4+i)==LOW?"255":"0");
    }
  }
''')

sketch('wifi_minimum',r'''
#include <WiFiS3.h> // Arduino UNO R4 Boards by Arduino

const char WIFI_SSID[] = "YOUR_WIFI";
const char WIFI_PASS[] = "YOUR_PASSWORD";

void setup() {
  Serial.begin(9600);

  // Block here until the first WiFi connection succeeds.
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connecting...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    delay(10000); // Wait before checking/retrying.
  }

  Serial.println("WiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Application code goes here. No automatic reconnect in this example.
}
''')

sketch('mqtt_minimum',r'''
#include <WiFiS3.h> // Arduino UNO R4 Boards by Arduino
#include <MQTT.h>   // MQTT by Joel Gaehwiler (256dpi)

const char WIFI_SSID[] = "YOUR_WIFI";
const char WIFI_PASS[] = "YOUR_PASSWORD";
const char BROKER[] = "mqtt-dashboard.com"; // Replace with exam broker.
const int MQTT_PORT = 1883;                // Plain MQTT TCP, not WebSocket.
const char CLIENT_ID[] = "YOUR_ID-bare";   // Must be unique.
const char MQTT_USER[] = "";              // Empty if not required.
const char MQTT_PASS[] = "";
const char SUB_TOPIC[] = "YOUR_ID/venus";
const char PUB_TOPIC[] = "YOUR_ID/temp";

WiFiClient network; // TCP transport; not the WiFi controller.
MQTTClient mqtt(256);

void messageReceived(String &topic, String &payload) {
  Serial.print("RX topic: ");
  Serial.println(topic);
  Serial.print("RX payload: ");
  Serial.println(payload);
  // Process incoming data here. Do not connect/subscribe/publish here.
}

void setup() {
  Serial.begin(9600);

  // 1. Connect WiFi first; keep trying until it succeeds.
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connecting...");
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    delay(10000);
  }
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());

  // 2. Configure the MQTT destination and incoming-message callback.
  mqtt.begin(BROKER, MQTT_PORT, network);
  mqtt.onMessage(messageReceived);

  // 3. Keep trying MQTT until the first connection succeeds.
  while (!mqtt.connect(CLIENT_ID, MQTT_USER, MQTT_PASS)) {
    Serial.println("MQTT connecting...");
    delay(1000);
  }
  Serial.println("MQTT connected");

  // 4. Subscribe only after connection. Check the returned result.
  if (mqtt.subscribe(SUB_TOPIC)) {
    Serial.println("Subscribed");
  } else {
    Serial.println("Subscribe failed");
  }

  // 5. Publish ONCE at startup, not continuously.
  mqtt.publish(PUB_TOPIC, "28.6");
}

void loop() {
  mqtt.loop(); // Process incoming messages and keep-alive frequently.
  // No WiFi/MQTT reconnect in this minimum example.
}
''')

CORE='ไม่ต้องติดตั้งไลบรารีเพิ่ม · ใช้ Arduino core / Arduino UNO R4 Boards โดย Arduino'
MQTT='MQTT — Joel Gaehwiler (256dpi), อ้างอิง 2.5.3 · #include <MQTT.h> หรือ <MQTTClient.h> · อย่าเลือก PubSubClient เพราะ API คนละชุด'
LCDLIB='LiquidCrystal I2C — Frank de Brabander · ผู้ดูแล Marco Schwartz · ชุด API lcd.init(), lcd.backlight(), lcd.setCursor() · Wire โดย Arduino มากับ board package'
PAGES=[]
def page(id,title,group,desc,**kwargs):
    PAGES.append(dict(id=id,title=title,group=group,desc=desc,**kwargs))
def device(id,title,desc,sk,pins,principle,formula='',tips=None,lib=CORE,calc=None,**kw):
    page(id,title,'อุปกรณ์',desc,codes=[sk],pins=pins,principle=principle,formula=formula,tips=tips or [],lib=lib,calc=calc,**kw)

device('hc-sr04','HC-SR04','วัดระยะทางด้วยเสียงสะท้อน · สไลด์ 14 หน้า 28–33 / Lab 14','ultrasonic',
 [['VCC','5V'],['TRIG','D4'],['ECHO','D2'],['GND','GND']],
 'ส่ง TRIG เป็น HIGH อย่างน้อย 10 µs แล้ววัดพัลส์ HIGH ของ ECHO ด้วย pulseIn() เวลาเป็น µs และเป็นเวลาเดินทางไป–กลับ จึงต้องหาร 2',
 'ระยะ (cm) = เวลา ECHO (µs) × 0.0343 ÷ 2\nตัวอย่าง: 1,000 × 0.0343 ÷ 2 = 17.15 cm\nสูตรในสไลด์ใช้ us / 29 / 2 ซึ่งเป็นค่าประมาณใกล้เคียงกัน',
 ['Serial Monitor ต้องเป็น 9600 baud','pulseIn() คืน 0 เมื่อ timeout: ตรวจ TRIG/ECHO, GND และทิศทางวัตถุ','ใช้ unsigned long เก็บเวลา ไม่ใช้ int แบบอ้างอิง AVR เดิม','0.0343 cm/µs ใช้ความเร็วเสียงประมาณ 343 m/s; ระยะจริงขึ้นกับอุณหภูมิ'],calc='ultrasonic',source='14:28-33')
device('mcp9700','MCP9700','วัดอุณหภูมิแบบ Analog · สไลด์ 14 หน้า 20–24 / Lab 14','mcp9700',
 [['VDD (1)','5V'],['VOUT (2)','A0'],['GND (3)','GND']],
 'แรงดันเอาต์พุตมี offset 0.5 V ที่ 0°C และเพิ่ม 0.01 V ต่อ 1°C ใช้ MCP9700 ตามเอกสาร ไม่แทนสูตรของ TMP36/LM35 โดยไม่ตรวจรุ่นและขา',
 'V = ADC × Vref / (2ⁿ − 1)\nT (°C) = (V − 0.5) / 0.01\nเช่น V = 0.75 V → T = 25°C',
 ['ดูหมายเลขขาและมุมมองจาก datasheet ก่อนเสียบ TO-92: ในสไลด์มีภาพ bottom view ด้วย','สูตรในสไลด์หน้า 23 มีวงเล็บคลาดเคลื่อน โค้ดนี้เขียนใหม่เป็น (V−0.5)×100','กำหนด ADC เป็น 10-bit และใช้ 5.0f เพื่อไม่หารแบบจำนวนเต็ม'],calc='mcp9700',source='14:20-24')
device('thermistor','NTC Thermistor TTC05103','วัดอุณหภูมิจากความต้านทาน · สไลด์ 14 หน้า 13–19 / Lab 14','thermistor',
 [['5V','R คงที่ 10kΩ'],['R 10kΩ อีกด้าน','จุด A0'],['A0','NTC ขาหนึ่ง'],['NTC อีกขา','GND']],
 'NTC ร้อนขึ้นแล้วความต้านทานลดลง ต่อ 5V → R คงที่ → A0 → NTC → GND ตามสไลด์ก่อนใช้สมการนี้ R₀=10kΩ ที่ 25°C และ B₂₅/₅₀=4050 K สำหรับ TTC05103',
 'Rntc = Rfixed × ADC / (ADCmax − ADC)\n1/T = 1/T₀ + ln(Rntc/R₀)/B\nT°C = T(K) − 273.15\nที่ ADC≈511.5 → R≈10kΩ → T≈25°C',
 ['ใช้รูปต้นฉบับ Lab 14 ตามที่ให้มา สาย Analog Input Pin ต่อ A0 และ GND ต่อ GND; ตัวอย่างนี้ใช้ 5V แม้ต้นฉบับมีป้าย 3.3V ปะปน','NTC ไม่มีขั้ว แต่ต้องไม่เสียบสองขาอยู่ในกลุ่มรูที่ต่อถึงกัน','หากสลับตำแหน่ง NTC กับ R คงที่ สูตร R ต้องเปลี่ยน','ADC=0 หรือ ADC=1023 ทำให้สมการใช้งานไม่ได้ ให้ตรวจสาย','ค่า B ขึ้นกับรุ่น ไม่คัดลอก 3950 จากตัวอย่างอื่นโดยอัตโนมัติ'],calc='thermistor',source='14:13-19')
device('ldr','LDR / Photoresistor','ตรวจแสงและเปิดไฟเมื่อมืด · สไลด์ 14 หน้า 8–12','ldr',
 [['5V','LDR ขาหนึ่ง'],['LDR อีกขา','A0'],['A0','R 10kΩ → GND'],['D4','R 220Ω → LED +'],['LED −','GND']],
 'แสงมากขึ้น → ความต้านทาน LDR ลดลง วงจรนี้วาง LDR ด้าน 5V จึงได้ ADC สูงเมื่อสว่างและต่ำเมื่อมืด ใช้ threshold ที่ทดลองวัดจริง',
 'Vout = Vcc × Rfixed / (Rldr + Rfixed)',
 ['ลองบังแสงและอ่าน Serial เพื่อเลือก threshold','ADC เป็นค่าดิบ ไม่ใช่หน่วย lux; การจะได้ lux ต้องมีข้อมูลสอบเทียบ','หากวงจรสลับด้าน ทิศทางเปรียบเทียบสว่าง/มืดจะกลับกัน'],source='14:8-12')
device('pot','Potentiometer → PWM','หมุนปรับความสว่าง LED · สไลด์ 13 หน้า 49–52 / Lab 13','pot_pwm',
 [['ขาริม 1','5V'],['ขากลาง (wiper)','A0'],['ขาริม 2','GND'],['D9','R 220Ω → LED +'],['LED −','GND']],
 'ขากลางให้แรงดันระหว่าง 0–5V ตามตำแหน่งหมุน อ่าน 10-bit ได้ 0–1023 แต่ PWM 8-bit รับ 0–255 ต้องแปลงช่วงก่อน',
 'PWM = map(ADC, 0, 1023, 0, 255)\nDuty (%) ≈ PWM / 255 × 100',
 ['ใช้ขาที่มีเครื่องหมาย ~ สำหรับ PWM: D3,5,6,9,10,11','หากตั้ง analogReadResolution(14) ต้องเปลี่ยน ADCmax เป็น 16383','A0 มี DAC ด้วย แต่โจทย์นี้ใช้เป็น ADC; analogWrite ที่ D9 เป็น PWM'],calc='adc',source='13:49-52')
device('pir','PIR Motion Sensor','ตรวจการเคลื่อนไหวแล้วเปลี่ยนสี RGB · สไลด์ 13 หน้า 18–19','pir',
 [['VCC','5V ตามสเปกโมดูล'],['OUT','D4'],['GND','GND'],['RGB common anode','5V'],['D3 / D5 / D6','R 330Ω แยกแต่ละสี → R/G/B']],
 'ตรวจการเปลี่ยนแปลงรังสีอินฟราเรดจากวัตถุอุ่น ตัวอย่างใช้ OUT HIGH เมื่อตรวจพบ แล้วแสดงสีเขียว มิฉะนั้นสีแดง',
 tips=['รอให้ PIR อุ่นตัวตามสเปกก่อนทดสอบ','ตรวจลำดับ VCC/OUT/GND บนโมดูลจริง ไม่อิงสีสายหรือรูปโมดูลอื่น','ไม่ใช้สมการแปลงเป็นระยะทาง'],source='13:18-19')
device('switch','Switch / INPUT_PULLUP','กดปุ่มควบคุม LED และลดการเด้ง · สไลด์ 13 หน้า 6–24','button',
 [['D4','ปุ่มข้างหนึ่ง'],['ปุ่มอีกข้าง','GND'],['D9','R 330Ω → LED +'],['LED −','GND']],
 'INPUT_PULLUP เปิดตัวต้านทานภายใน: ปล่อยปุ่มอ่าน HIGH กดอ่าน LOW ไม่ปล่อย input ลอย Pull-down ภายนอกจะให้ตรรกะกลับกัน',
 tips=['ปุ่ม 4 ขามักมีสองขาที่ต่อถึงกันอยู่แล้ว ตรวจด้านก่อนเสียบคร่อมร่อง breadboard','หากโจทย์ต้องกดครั้งเดียวสลับสถานะ ใช้ตัวอย่าง debounce ด้านล่าง','อย่าใช้ delay ยาว debounce ในโปรแกรม MQTT'],extra_codes=['debounce'],source='13:6-24')
device('keypad','Keypad 4×4','สแกนปุ่มด้วยแถว–คอลัมน์ · สไลด์ 13 หน้า 22–29','keypad',
 [['R1 / R2 / R3 / R4','D6 / D7 / D8 / D9'],['C1 / C2 / C3 / C4','D2 / D3 / D4 / D5']],
 'ตั้ง rows เป็น INPUT_PULLUP แล้วดึง column ทีละเส้นเป็น LOW ถ้า row ใดอ่าน LOW แสดงว่ากดจุดตัดนั้น ปล่อย column อื่นเป็น input เพื่อไม่ขับสัญญาณสวนกัน',
 tips=['ไม่ใช้ไลบรารี Keypad เพิ่ม ตัวอย่างทำตามหลักสแกนในสไลด์','ต้องดูผังสายแถว–คอลัมน์ของ keypad จริง ลำดับหัวต่ออาจต่างกัน','ตัวอย่างรองรับการกดหนึ่งปุ่ม ไม่รับประกันหลายปุ่มพร้อมกัน/ghosting'],source='13:22-29')
device('led','LED / Blink','ไฟกระพริบและพื้นฐาน output · สไลด์ 12 หน้า 67–79 / Lab 12','led_blink',
 [['D9','R 220–330Ω'],['R อีกข้าง','LED anode (+)'],['LED cathode (−)','GND']],
 'LED เปล่งแสงเมื่อมีกระแสไหลถูกทิศ ต้องมีตัวต้านทานอนุกรม คาบคือเวลาติดรวมเวลาดับ',
 'f (Hz) = 1000 / (Ton + Toff) เมื่อเวลาเป็น ms\nR ≈ (Vcc − Vf) / I',
 ['ขายาวมักเป็น anode; ด้านแบนมักเป็น cathode แต่ควรตรวจชิ้นส่วนจริง','ใช้ตัวคำนวณแถบสีตรวจค่า R ก่อนต่อ'],calc='resistor',source='12:67-79')
device('rgb','RGB LED — Common Anode','ผสมสี 7 สี · สไลด์ 12 หน้า 80 / Lab 12','rgb_colors',
 [['ขาร่วม anode','5V'],['Cathode สี R','R 330Ω → D3'],['Cathode สี G','R 330Ω → D5'],['Cathode สี B','R 330Ω → D6']],
 'RGB ที่แจกใน Lab 12 เป็น Common Anode การดึงขาสี LOW ทำให้ติด จึงกลับค่า PWM ด้วย 255−value เพื่อให้ค่า RGB 0=ดับ และ 255=สว่างสุด',
 'Common anode: output PWM = 255 − desired\nR+B = ม่วง, R+G = เหลือง, G+B = ฟ้า, R+G+B = ขาว',
 ['ใช้ตัวต้านทานแยกทุกสี ไม่ใช้ R ตัวเดียวที่ขาร่วม','ลำดับขา R/G/B ไม่เหมือนกันทุกตัว ต้องตรวจจริง','Common cathode ต่อขาร่วม GND และใช้ analogWrite(pin,value) โดยไม่กลับค่า'],source='12:80')
device('seven','7-segment 1 หลัก','แสดงตัวเลข 0–9 · สไลด์ 12 หน้า 82–84 / Lab 12','seven_one',
 [['a,b,c,d,e,f,g','R 330Ω แยกเส้น → D2,3,4,5,6,7,8'],['Common cathode','GND'],['dp','ไม่ใช้ในตัวอย่าง']],
 'แต่ละ segment เป็น LED หนึ่งชุด โค้ดนี้ใช้ Common Cathode และตารางบิตเรียง a,b,c,d,e,f,g ค่า 1=ติด',
 tips=['ดูหมายเลขขาของชิ้นส่วนจริงก่อน map a–g; ไม่สมมติว่า pin1 คือ a','ถ้าเป็น Common Anode ต้องกลับตรรกะและต่อขาร่วม 5V','ตัวต้านทานต้องแยกทุก segment'],source='12:82-84')
device('seven2','7-segment 2 หลัก','Multiplexing แสดงรหัสนักศึกษา · Lab 12','seven_two',
 [['a,b,c,d,e,f,g ร่วมสองหลัก','R 330Ω แยกเส้น → D2–D8'],['CC หลักซ้าย','Collector ของ NPN 1'],['CC หลักขวา','Collector ของ NPN 2'],['Emitter NPN ทั้งคู่','GND'],['D10 / D11','R 1kΩ → Base NPN 1/2']],
 'ปิดทั้งสองหลักก่อนเปลี่ยน pattern แล้วเปิดทีละหลักทุก 2 ms ตาจึงเห็นสองหลักพร้อมกัน ใช้ทรานซิสเตอร์ช่วยรับกระแสรวมของแต่ละ common cathode',
 'สลับทุก 2 ms → หนึ่งรอบสองหลัก 4 ms ≈ 250 Hz',
 ['อุปกรณ์ NPN และ R base เป็นส่วนเสริมของวงจรตัวอย่างเพื่อไม่ให้ขา MCU รับกระแสรวมโดยตรง ตรวจ pinout B/C/E ตามรุ่นจริง','เปลี่ยน idPairs ให้เป็นรหัสนักศึกษาของตัวเอง','อย่า delay(1000) เพื่อสลับคู่เลข เพราะจะหยุดการ multiplex ใช้ millis()','ตารางขาด้านบนและ seven_two.ino เป็นแบบ NPN เปิดหลักด้วย HIGH ส่วนรูปที่ผู้ใช้ส่งและ seven_two_direct.ino ต่อตรง เปิดหลักด้วย LOW ห้ามสลับวงจร','ตัวอย่างต่อตรง: a,b,c,d,e,f,g = D4,D5,D8,D6,D7,D3,D2; DP=D9 ปิดไว้; common ซ้าย/ขวา=D10/D11 สแกนทุก 5 ms รอบละ 10 ms หรือ 100 Hz แสดงคู่เลขละ 500 ms','ต่อตรงต้องตรวจขีดจำกัดกระแสรวม common/GPIO จากบอร์ดจริง; รหัสต้องเป็นตัวเลขและมีจำนวนหลักคู่'],extra_codes=['seven_two_direct'],source='12:83-84')
device('lcd','LCD 16×2 I2C','ข้อความ ตัวเลข และ custom characters · สไลด์ 14 หน้า 36–51','lcd_hello',
 [['GND','GND'],['VCC','5V'],['SDA','A4 / SDA'],['SCL','A5 / SCL']],
 'PCF8574 รับข้อมูล I2C แล้วขับ LCD ใช้สองสายสัญญาณร่วมกับ address เฉพาะอุปกรณ์ แถวและคอลัมน์เริ่มนับจาก 0: setCursor(0,1) คือแถวสอง',
 tips=['ค้น LiquidCrystal I2C โดย Frank de Brabander ตรวจผู้พัฒนาก่อนโหลด เพราะชื่อ header เดียวกันมีหลายไลบรารี','ตัวอย่างนี้ใช้ API ของชุด Frank/Marco และอ้างอิง 1.1.2; upstream master ระบุ 1.1.4/architectures=avr จึงอาจมี warning บน R4 ต้องตรวจ compile บนเครื่องจริง','รัน I2C scanner ก่อน อย่าเดาว่าทุกจอเป็น 0x27','ไฟติดแต่ไม่เห็นตัวอักษร: หมุน contrast ที่ backpack และตรวจ address','ข้อความใหม่สั้นกว่าเก่าต้องลบช่องท้าย; ไม่ clear() ทุก loop เพื่อลดกระพริบ'],lib=LCDLIB,extra_codes=['i2c_scanner','lcd_custom'],source='14:36-51')
device('ir-sound','IR / Sound Digital Module','ตัวอย่างการใช้ digitalRead · สไลด์ 13 หน้า 17','digital_module',
 [['VCC','ไฟตามสเปกโมดูล'],['GND','GND'],['Digital OUT','D4'],['D9','R 330Ω → LED + → GND']],
 'โมดูลตัวอย่างในสไลด์ให้ LOW เมื่อตรวจพบวัตถุหรือเสียง ใช้ digitalRead() ไม่แปลงเป็นหน่วยระยะทางหรือเดซิเบล',
 tips=['หมุน potentiometer บนโมดูลเพื่อตั้ง threshold','ต้องตรวจ active level และแรงดัน OUT ของรุ่นจริง','เป็นตัวอย่างประกอบในสไลด์ ไม่ใช่โจทย์หลักใน README Lab 13'],source='13:17')

def lab(id,title,desc,codes,pins,**kw):
    page(id,title,'ตัวอย่างแลบ',desc,codes=codes,pins=pins,lib=kw.pop('lib',CORE),**kw)
lab('lab12','Lab 12 — LED, RGB, 7-segment','ครบสี่งาน: ไฟกระพริบ, RGB 7 สี, เลข 0–9 และแสดงรหัสสองหลัก',[],[],links=['led','rgb','seven','seven2'],principle='เปิดตัวอย่างแต่ละงานเพื่อดูวงจรและโค้ดครบ ไม่ใช้ขาของทุกตัวอย่างพร้อมกันโดยไม่วางแผนใหม่',tips=['RGB ของแลบเป็น Common Anode','งานสองหลักใช้ multiplexing และเปลี่ยนรหัสให้เป็นของตัวเอง'])
lab('lab13','Lab 13 — ADC และ LED fading','Potentiometer ควบคุม LED และ LED สี่ดวงที่จังหวะต่างกัน',['fading4'],[['LED1 / LED2 / LED3 / LED4','D3 / D5 / D6 / D9 ผ่าน R 330Ω แต่ละดวง'],['LED cathode ทุกดวง','GND']],links=['pot'],principle='LED1 จากดับไปเต็ม, LED2 เร็วสองเท่า, LED3 เต็มไปดับ และ LED4 ครึ่งไปเต็ม ตัวอย่างใช้ triangle wave เพื่อวนกลับต่อเนื่อง โดยช่วงขาขึ้น/ลงเป็นไปตามโจทย์ ใช้ millis() ไม่ให้ดวงหนึ่งหยุดอีกดวง',tips=['หากต้องการ ramp แล้วกระโดดกลับแทน triangle ให้ปรับฟังก์ชันสร้างเฟสตามเงื่อนไขโจทย์'])
lab('lab14','Lab 14 — Sensor → Serial','สามโจทย์หลัก: HC-SR04, MCP9700 และ Thermistor',[],[],links=['hc-sr04','mcp9700','thermistor'],principle='README ให้แสดงผลผ่าน Serial Monitor ส่วน LCD เป็นเนื้อหาต่อเนื่องในสไลด์',tips=['ตั้ง baud ให้ตรง 9600','เริ่มจากทดสอบ Sensor เดี่ยว ก่อนเพิ่ม LCD หรือ MQTT'])
lab('temp-lcd','อุณหภูมิ → LCD','MCP9700 อ่านค่าแล้วแสดงทศนิยมสองตำแหน่งตามสไลด์',['temp_lcd'],[['MCP9700 VDD / VOUT / GND','5V / A0 / GND'],['LCD VCC / GND','5V / GND'],['LCD SDA / SCL','A4 / A5']],lib=LCDLIB,principle='อ่าน ADC เป็นอุณหภูมิแล้วใช้ lcd.print(temp,2) สำหรับสองตำแหน่ง',links=['mcp9700','lcd'])
lab('keypad-seven','Keypad → 7-segment','ตัวอย่างรวมตามสไลด์ 13 โดยจัดขาใหม่ไม่ให้ชนกัน',['keypad_seven'],[['Keypad R1–R4','A0,A1,A2,A3'],['Keypad C1–C4','D2,D3,D4,D5'],['7-segment a–g','D6–D12 ผ่าน R แยกเส้น'],['7-segment CC','GND']],principle='รับเฉพาะปุ่ม 0–9 แล้วแสดงเลขนั้น ปุ่ม A–D,*,# ไม่เปลี่ยนจอ ใช้ analog pins เป็น digital inputs ได้',tips=['ห้ามใช้ผังขา keypad เดี่ยว D6–D9 ร่วมกับ segments D6–D12 จะชนกัน'])
lab('mqtt-pot','Potentiometer → MQTT → LED','Lab 15 · หมุนที่บอร์ดส่งเพื่อหรี่ไฟที่บอร์ดรับ',['mqtt_pot_tx','mqtt_pwm_rx'],[],lib=MQTT,pair=True,roles=['ฝั่งส่ง · Potentiometer','ฝั่งรับ · LED PWM'],wiring=[[['ขาริม / ขากลาง / ขาริม','5V / A0 / GND']],[['D9','R 220Ω → LED +'],['LED −','GND']]],contract=[['Broker / TCP port','mqtt-dashboard.com / 1883 (หรือค่าที่อาจารย์กำหนด)'],['Topic','physcom/YOUR_ID/brightness'],['Payload','ข้อความตัวเลข 0–255 เช่น "128"'],['Client ID','YOUR_ID-tx และ YOUR_ID-rx ห้ามซ้ำ']],principle='ฝั่งส่ง map ค่า ADC 0–1023 เป็น PWM 0–255 แล้วส่งเป็น String ฝั่งรับตรวจข้อความก่อนแปลงเป็นตัวเลข',tips=['หมุนแล้ว Serial ฝั่งส่งควรเปลี่ยน 0–255','ใช้ client ID ต่างกัน แต่ Topic ตรงกันรวมตัวพิมพ์เล็กใหญ่','Broker ตัวอย่างไม่ได้รับประกันว่าออนไลน์ในวันสอบ'])
lab('mqtt-keypad','Keypad → MQTT → LCD','Lab 15 · ส่งปุ่มหนึ่งตัวไปแสดงบนจออีกบอร์ด',['mqtt_keypad_tx','mqtt_lcd_rx'],[],lib=MQTT+'\n'+LCDLIB,pair=True,roles=['ฝั่งส่ง · Keypad','ฝั่งรับ · LCD'],wiring=[[['R1–R4','D6–D9'],['C1–C4','D2–D5']],[['LCD VCC / GND','5V / GND'],['SDA / SCL','A4 / A5']]],contract=[['Topic','physcom/YOUR_ID/key'],['Payload','ตัวอักษรหนึ่งตัว เช่น "5" หรือ "A"'],['Client ID','YOUR_ID-tx / YOUR_ID-rx']],principle='ส่งเมื่อเกิดเหตุการณ์กดปุ่มหลัง debounce ฝั่งรับล้างช่องข้อความเดิมแล้วเขียน payload ลง LCD',tips=['ถ้า MQTT รับได้แต่จอว่าง ให้ทดสอบ lcd_hello และ scanner แยกก่อน'])
lab('mqtt-temp','อุณหภูมิ → MQTT → LCD / RGB','ตัวอย่างประยุกต์ตามสไลด์ 15 หน้า 68',['mqtt_temp_tx','mqtt_temp_lcd_rx','mqtt_temp_rgb_rx'],[],lib=MQTT+'\n'+LCDLIB,roles=['MCP9700 sender','LCD receiver','RGB receiver ทางเลือก'],contract=[['Topic','physcom/YOUR_ID/temperature'],['Payload','เลขอุณหภูมิเป็นข้อความ เช่น "25.54"'],['จุดเปลี่ยนสี RGB','≥30°C สีแดง, ต่ำกว่าเป็นสีเขียว']],principle='เลือก receiver ตามโจทย์ หากเปิดทั้งสอง receiver พร้อมกันต้องแก้ Client ID ให้ไม่ซ้ำ โค้ดแปลงค่าไว้สำหรับข้อความตัวเลขจาก sender ตัวอย่างนี้',links=['mcp9700','lcd','rgb'],wiring=[[['MCP9700 VDD / VOUT / GND','5V / A0 / GND']],[['LCD VCC / GND / SDA / SCL','5V / GND / A4 / A5']],[['RGB common anode','5V'],['RGB R / G / B','D3 / D5 / D6 ผ่าน R แยกเส้น']]],pair=True,tips=['ใช้ toFloat() ไม่ใช้ toInt() เพราะต้องการทศนิยม','ตั้ง client ID ของ LCD กับ RGB ต่างกันถ้าใช้พร้อมกัน'])
lab('mqtt-web','เว็บ → MQTT → RGB','Lab 15 · ควบคุมสีแยก R/G/B ด้วยปุ่มหรือ slider',['mqtt_rgb_rx'],[['RGB common anode','5V'],['R / G / B cathode','D3 / D5 / D6 ผ่าน R 330Ω แต่ละเส้น']],lib=MQTT,contract=[['Topics','physcom/YOUR_ID/rgb/r, /g, /b'],['Payload','ข้อความ 0–255; ON=255, OFF=0'],['Subscribe filter','physcom/YOUR_ID/rgb/+']],principle='ใช้เว็บตัวอย่างในหมวดเว็บส่ง MQTT over WebSocket ฝั่งบอร์ดรับผ่าน TCP และกลับค่า PWM สำหรับ Common Anode',links=['web-examples','mqtt-sim','rgb'],tips=['คอมออฟไลน์ใช้โหมดจำลองได้ แต่ส่ง Broker จริงไม่ได้','พอร์ต WebSocket ไม่ใช่ TCP 1883 ให้ใช้ค่าที่ Broker เปิดไว้'])
lab('mqtt-switch','Switch 3 ตัว → MQTT → RGB','ตัวอย่างประยุกต์สไลด์ 15 หน้า 68',['mqtt_switch_tx','mqtt_rgb_rx'],[],lib=MQTT,pair=True,roles=['ฝั่งส่ง · Switch','ฝั่งรับ · RGB'],wiring=[[['Switch 1/2/3','D4/D5/D6 → ปุ่ม → GND']],[['RGB common anode','5V'],['R/G/B','D3/D5/D6 ผ่าน R แยกเส้น']]],contract=[['Topics','physcom/YOUR_ID/rgb/r, /g, /b'],['Payload','255 เมื่อกด, 0 เมื่อปล่อย']],principle='ใช้ INPUT_PULLUP ทั้งสามปุ่มและส่งสถานะแต่ละสี ทุก 200 ms ฝั่งรับใช้ rgb subscriber เดียวกับเว็บ')

page('wifi-minimum','WiFi — Bare minimum','MQTT','เริ่มจาก WiFi อย่างเดียว: วนเชื่อมต่อครั้งแรกจนสำเร็จ พร้อมคำอธิบายทีละส่วน',codes=['wifi_minimum'],lib='WiFiS3 — Arduino · มากับ Arduino UNO R4 Boards ไม่ต้องติดตั้งแยก',walkthrough=[
 {'title':'โค้ดนี้ทำอะไรบ้าง','body':'เปิดบอร์ด → เริ่ม Serial → วนพยายามเข้า Hotspot จนสำเร็จ → แสดง IP → เข้า loop() ที่ว่างอยู่ ไม่มี MQTT และไม่มีการอ่านเซนเซอร์ จึงเหมาะสำหรับแยกตรวจว่าบอร์ดเข้า WiFi ได้ก่อนเพิ่มงานอื่น'},
 {'title':'แก้แค่ชื่อ WiFi กับรหัสผ่านก่อน','body':'แทน YOUR_WIFI และ YOUR_PASSWORD ด้วยชื่อเครือข่ายและรหัสผ่านจริง รวมตัวพิมพ์เล็กใหญ่และช่องว่าง ถ้าตั้งผิด setup() จะวนรอไม่จบ สำหรับ Hotspot ให้ตรวจว่าเปิดโหมดที่บอร์ดรองรับ โดยเริ่มทดสอบที่ 2.4 GHz'},
 {'title':'#include <WiFiS3.h> คืออะไร','body':'ดึงคำประกาศจากไลบรารี WiFiS3 ที่มากับแพ็กเกจ Arduino UNO R4 Boards โดย Arduino เลือกบอร์ด Arduino UNO R4 WiFi ใน IDE ก่อน สไลด์ 15 หน้า 62 สอน WiFiS3; ไม่ต้องค้นลงไลบรารี WiFi ที่ชื่อคล้ายกัน'},
 {'title':'WiFi เป็นอ็อบเจกต์ที่มีให้แล้ว ไม่ต้องสร้างเอง','body':'ในไลบรารีมีอ็อบเจกต์ WiFi ให้เรียกใช้อยู่แล้ว ชื่อ WiFi ใน WiFi.begin() และ WiFi.status() จึงไม่ใช่การเรียกผ่านชื่อคลาส และไม่ใช่อ็อบเจกต์ที่เราต้องประกาศ WiFiClient network ใช้เมื่อต้องมีการเชื่อมต่อ TCP กับเซิร์ฟเวอร์ ตัวอย่าง WiFi อย่างเดียวนี้ยังไม่ต้องสร้าง network'},
 {'title':'WiFi.status() คืนค่าอะไร','body':'คืนรหัสสถานะการเชื่อมต่อ เช่น WL_CONNECTED, WL_IDLE_STATUS, WL_NO_SSID_AVAIL ไม่ใช่จำนวนอุปกรณ์ ไม่ใช่ IP และไม่ใช่ true/false เสมอไป จึงเทียบกับ WL_CONNECTED โดยตรง: != แปลว่ายังไม่อยู่ในสถานะที่เชื่อมต่อสำเร็จ'},
 {'title':'while ทำให้เชื่อมต่อครั้งแรกจนสำเร็จอย่างไร','body':'while ตรวจเงื่อนไขก่อนแต่ละรอบ ถ้ายังไม่เชื่อม ให้สั่ง WiFi.begin() แล้วเว้นเวลา 10 วินาที จากนั้นกลับไปตรวจใหม่ หากเชื่อมแล้วเงื่อนไขเป็น false จึงข้ามออกมาพิมพ์ WiFi connected การที่ begin() ถูกเรียกไม่ได้รับประกันว่าเชื่อมสำเร็จ ต้องตรวจสถานะหรือผลลัพธ์ด้วย'},
 {'title':'delay(10000) จำเป็นแค่ไหน','body':'ใช้เว้นจังหวะให้การเชื่อมต่อและการลองซ้ำ ไม่ใช่คำสั่งเชื่อมต่อ และไม่ได้ยืนยันว่า WiFi ต้องใช้เวลา 10 วินาทีทุกครั้ง ระหว่าง delay โปรแกรมส่วนอื่นของ sketch ยังไม่เดินต่อ แม้เครือข่ายจะเชื่อมสำเร็จก่อนครบเวลานี้'},
 {'title':'setup() กับ loop() ต่างกันอย่างไร','body':'setup() ทำครั้งเดียวหลังเปิดเครื่องหรือรีเซ็ต โค้ดจะยังไม่ถึง loop() จนกว่า setup() จะจบ ตัวอย่างนี้จงใจรอ WiFi ใน setup() เพื่อให้ดูง่าย ไม่ใช่แบบที่ทำงานอื่นพร้อมกับรอเครือข่าย หาก WiFi หลุดทีหลัง ตัวอย่างนี้ไม่มีโค้ดวนกลับมาต่อใหม่'},
 {'title':'IP ที่แสดงพิสูจน์อะไร','body':'WiFi.localIP() อ่าน IP ของบอร์ดในเครือข่าย เช่น 192.168.43.20 การเชื่อม Hotspot และมี IP ไม่ได้ยืนยันว่าออกอินเทอร์เน็ตได้หรือ Broker เข้าถึงได้ ขั้น WiFi กับ MQTT เป็นคนละขั้น หากต่อ Broker ในเครือข่ายเดียวกันอาจไม่ต้องใช้อินเทอร์เน็ต'},
 {'title':'Serial เป็นแค่เครื่องมือดูผล','body':'Serial.begin(9600) กำหนดการสื่อสารกับ Serial Monitor และ print/println ใช้แสดงสถานะ ไม่ได้เป็นตัวต่อ WiFi ตั้ง Serial Monitor ที่ 9600 หากเปิดดูช้าอาจพลาดข้อความช่วงเริ่ม ให้รีเซ็ตบอร์ดเพื่อดูใหม่ ตัวอย่างไม่รอ while(!Serial) จึงเริ่มทำงานได้แม้ไม่ได้เปิด Monitor'},
 {'title':'ต่างจาก maintainConnection() ในเว็บอย่างไร','body':'แบบขั้นต่ำนี้รอครั้งแรกให้สำเร็จ แล้วไม่ตรวจต่อใหม่ใน loop() ส่วน maintainConnection() เป็นฟังก์ชันที่ผู้จัดทำเว็บเขียนเพิ่ม ใช้ตรวจ WiFi/MQTT และเว้นช่วงลองใหม่ระหว่างทำงาน ไม่ใช่ API ที่ Arduino มีให้โดยตรง ทั้งนี้ WiFi.begin() และ MQTT connect() เองอาจใช้เวลารอ จึงไม่ควรเรียกแบบเดิมว่าไม่บล็อกทั้งหมด'},
],links=['mqtt-minimum','setup','troubleshooting'],tips=['ทดสอบให้ขึ้น WiFi connected และแสดง IP ก่อนค่อยเพิ่ม MQTT','ไม่ต้องต่อเซนเซอร์เพื่อทดสอบหน้านี้','ไม่มี timeout รวม: ชื่อ WiFi ผิดหรือ Hotspot ปิด โค้ดจะรอต่อไปตามที่ตั้งใจ'])

page('mqtt-minimum','MQTT — Bare minimum','MQTT','โค้ดครบ WiFi → Broker → Subscribe/Publish → Callback พร้อมคำอธิบายหนัก ๆ',codes=['mqtt_minimum'],lib='WiFiS3 — Arduino (มากับ Arduino UNO R4 Boards)\n'+MQTT,walkthrough=[
 {'title':'อ่านลำดับก่อน: เชื่อม WiFi แล้วจึงเชื่อม MQTT','body':'setup() ทำตามลำดับ: WiFi สำเร็จ → mqtt.begin() ระบุปลายทาง → mqtt.onMessage() ลงทะเบียน callback → วน mqtt.connect() จนสำเร็จ → Subscribe → Publish หนึ่งครั้ง → เข้า loop() เรียก mqtt.loop() บ่อย ๆ หน้านี้ตัดระบบต่อใหม่ระหว่างทำงานออกเพื่อให้เห็นแกนหลัก'},
 {'title':'รายการที่ต้องแก้ตามโจทย์','body':'แก้ WIFI_SSID/WIFI_PASS, BROKER/MQTT_PORT, CLIENT_ID, MQTT_USER/MQTT_PASS, SUB_TOPIC/PUB_TOPIC และข้อความที่ Publish ตัวอย่าง broker เป็นเพียงค่าประกอบ ไม่รับประกันว่าเปิดให้บริการวันสอบ Topic ไม่ได้เติมรหัสนักศึกษาให้อัตโนมัติ: YOUR_ID/venus ต้องแก้เป็นรหัสจริง เช่น 68070015/venus และ CLIENT_ID ต้องไม่ซ้ำ client อื่น'},
 {'title':'WiFi / network / mqtt เป็นคนละตัว','body':'WiFi เป็นอ็อบเจกต์ของไลบรารี ใช้เข้าเครือข่ายและตรวจ WiFi.status() ส่วน WiFiClient network คืออ็อบเจกต์ TCP ที่เราสร้างเพื่อเป็นช่องทางคุยกับเซิร์ฟเวอร์ และ MQTTClient mqtt(256) คือผู้จัดการโปรโตคอล MQTT ใช้ช่องทาง network อีกที ชื่อ network และ mqtt เปลี่ยนได้ แต่ต้องแก้จุดที่ใช้งานให้ตรงกัน เลข 256 คือการตั้งขนาดบัฟเฟอร์ของไลบรารี ไม่ใช่พอร์ตหรือ Client ID'},
 {'title':'mqtt.begin() ยังไม่ได้ต่อ Broker','body':'mqtt.begin(BROKER, MQTT_PORT, network) ตั้งปลายทางและผูก network ให้ MQTT ใช้ ส่วน mqtt.connect() เป็นคำสั่งที่พยายามสร้างการเชื่อมต่อจริง จึงต้องใช้ทั้งสอง ไม่ใช่เรียก begin() แล้วถือว่าเชื่อมสำเร็จ'},
 {'title':'ทำไมใช้ while (!mqtt.connect(...))','body':'connect() คืน true เมื่อเชื่อม MQTT สำเร็จ และ false เมื่อล้มเหลว เครื่องหมาย ! กลับค่าตรรกะ จึงวนรอเมื่อยังเชื่อมไม่ได้ delay(1000) เว้นก่อนลองครั้งต่อไป เมื่อสำเร็จจึงออกจาก while จุดนี้ค้างรอได้เรื่อย ๆ ถ้า Broker ปิด ที่อยู่ผิด หรือ authentication ไม่ผ่าน และถ้า WiFi หลุดระหว่างรอ MQTT ตัวอย่างนี้ไม่ได้ย้อนกลับไปต่อ WiFi ใหม่'},
 {'title':'Client ID ไม่ใช่ Topic หรือชื่อ WiFi','body':'CLIENT_ID ใช้ระบุตัว client ต่อ Broker คนละอย่างกับชื่อ Topic ที่รับส่ง Client ID ของสองบอร์ดต้องต่างกัน แต่ Topic สำหรับส่งหากันต้องตรงกัน สำหรับ public broker ที่ไม่ต้องยืนยันตัวตน ใช้ username/password ว่างตามค่าตัวอย่าง หากอาจารย์กำหนดให้ล็อกอินให้กรอกข้อมูลจริงแทน'},
 {'title':'subscribe() ต้องทำหลัง connect สำเร็จ','body':'mqtt.subscribe(SUB_TOPIC) ขอให้ Broker ส่งข้อความของ Topic นั้นมาให้ โค้ดตรวจผลคืนค่าเพื่อแจ้งว่า Subscribe สำเร็จหรือไม่ หากไม่สำเร็จจะพิมพ์ Subscribe failed และไม่ได้ retry subscription เพิ่มในตัวอย่างขั้นต่ำ ข้อความที่ส่งก่อน Subscribe จะไม่ถูกส่งย้อนหลังตามปกติ เว้นแต่ใช้ retained message หรือ session ที่เกี่ยวข้อง'},
 {'title':'onMessage() เป็นการลงทะเบียน ไม่ใช่รับข้อความทันที','body':'mqtt.onMessage(messageReceived) บอกไลบรารีว่ามีข้อความเข้าให้เรียกฟังก์ชันชื่อ messageReceived ชื่อนี้ตั้งเองได้ แต่ต้องตรงกับชื่อที่ลงทะเบียน ไม่ใส่วงเล็บ messageReceived() เพราะตรงนี้ต้องส่งตัวฟังก์ชัน ไม่ใช่สั่งเรียกเอง ฟังก์ชันรับ String &topic และ String &payload ตามรูปแบบของไลบรารี เครื่องหมาย & หมายถึงรับอ้างอิง String ที่ไลบรารีส่งมา'},
 {'title':'ข้อความเดินทางเข้า callback อย่างไร','body':'Publisher → Broker → subscription ของบอร์ด → ไลบรารีประมวลผล → messageReceived(topic,payload) ตัวแปร topic คือชื่อหัวข้อ เช่น 68070015/venus ส่วน payload คือข้อมูล เช่น 22 ถ้าจะควบคุม RGB ให้แปลงค่าแล้วตัดสินใจใน callback ไม่ต้องมี Serial.read() เพราะข้อมูลนี้เข้าจากเครือข่าย ไม่ใช่ช่องพิมพ์ Serial Monitor'},
 {'title':'Subscribe หลาย Topic ใช้ callback เดียวได้','body':'เพิ่ม subscribe ทีละ Topic หลัง connect แล้วแยกเงื่อนไขตาม topic ใน callback ชื่อ callback ไม่ต้องแยกตามจำนวน Topic ตัวอย่างด้านล่างเป็นส่วนที่นำไปแทน/เติมใน sketch หลัก ต้องเปลี่ยนรหัสและต่ออุปกรณ์ตามโค้ดแสดงผลของตนเอง','code':'// Add after MQTT connects:\nmqtt.subscribe("68070015/venus");\nmqtt.subscribe("68070015/prob_stat");\n\n// Replace the callback with topic routing:\nvoid messageReceived(String &topic, String &payload) {\n  if (topic == "68070015/venus") {\n    // Validate payload, then set RGB.\n  } else if (topic == "68070015/prob_stat") {\n    // Validate 0-9, then show on 7-segment.\n  }\n}'},
 {'title':'payload เป็นข้อความ แม้หน้าตาเป็นตัวเลข','body':'ใช้ payload.toInt() เมื่อต้องการจำนวนเต็ม และ payload.toFloat() เมื่อต้องการทศนิยม แต่ไม่ใช่ตัวตรวจความถูกต้อง ถ้าข้อความผิดรูปแบบอาจได้ 0 หรือแปลงได้เพียงส่วนต้น สำหรับโจทย์ 7-segment ที่กำหนดตัวเลขหนึ่งตัว ใช้ตรวจความยาวและช่วงตัวอักษรให้ชัดก่อนแปลง','code':"if (payload.length() == 1 && payload[0] >= '0' && payload[0] <= '9') {\n  int digit = payload[0] - '0';\n  // showDigit(digit); // Use your existing 7-segment function.\n}"},
 {'title':'publish() ใน setup() ส่งแค่ครั้งเดียว','body':'mqtt.publish(PUB_TOPIC, "28.6") ส่งข้อความ 28.6 ไปยัง Topic ที่ระบุ ไม่ได้ไปยัง Client ID ของอีกเครื่อง ในตัวอย่างนี้อยู่ setup() จึงส่งครั้งเดียวหลังเชื่อม ถ้าไม่มี Subscriber อยู่ตอนนั้นและไม่ได้ retain ผู้รับใหม่จะไม่ได้ข้อความนั้น ตัวอย่างใช้ QoS 0 และไม่ retain ตามค่าเริ่มต้น'},
 {'title':'อยากส่งค่าทุกหนึ่งวินาทีให้ใช้ millis()','body':'เพิ่มตัวแปร global และแทน loop() ตามตัวอย่างนี้ เพื่อให้ mqtt.loop() ยังถูกเรียกถี่ ระหว่างรอครบหนึ่งวินาที แทน 28.6 ด้วย String ของค่าที่อ่านได้จากเซนเซอร์จริง ไม่ใช้ delay ยาวใน loop เมื่อยังต้องรอรับข้อมูล','code':'// Global variable:\nunsigned long lastSend = 0;\n\nvoid loop() {\n  mqtt.loop();\n  if (mqtt.connected() && millis() - lastSend >= 1000UL) {\n    lastSend = millis();\n    mqtt.publish(PUB_TOPIC, "28.6");\n  }\n}'},
 {'title':'mqtt.loop() ไม่ใช่ตัวเชื่อมต่อใหม่','body':'mqtt.loop() ประมวลผลข้อมูลเข้าและงานดูแลการเชื่อมต่อ เช่น Keep Alive แต่ไม่ได้เรียก connect() ให้อัตโนมัติ ต้องเรียกบ่อยใน loop() หลีกเลี่ยง delay ยาวและ callback ที่ค้างรอ ไลบรารีอาจเรียก callback ระหว่างบางคำสั่งที่รอ ACK ด้วย ไม่ได้เกิดเฉพาะใน loop() เท่านั้น'},
 {'title':'ใน callback ทำอะไรได้บ้าง','body':'อ่าน topic/payload, เปลี่ยนตัวแปร, สั่ง GPIO สั้น ๆ หรืออัปเดตจอได้ แต่หลีกเลี่ยงการ connect/subscribe/publish ซ้อนใน callback ของไลบรารีนี้ ถ้าต้องส่งตอบ ให้เก็บข้อมูล/ตั้ง flag แล้วส่งใน loop() หลัง mqtt.loop() จบ หากเก็บไว้ใช้ภายหลังให้คัดลอก String อย่าเก็บ reference ของพารามิเตอร์ callback ไว้'},
 {'title':'ต้องการรับอย่างเดียวหรือส่งอย่างเดียว','body':'รับอย่างเดียว: ลบ publish() ออกจาก setup() ได้ แต่คง onMessage(), callback, subscribe() และ mqtt.loop() ส่งอย่างเดียว: ลบ onMessage(), callback และ subscribe() ได้ แต่ยังต้องคง mqtt.loop() เพื่อดูแลการเชื่อมต่อ และวาง publish() ในจังหวะที่โจทย์ต้องการ'},
 {'title':'WiFi หลุดหรือ MQTT หลุดหลัง setup() จะเกิดอะไร','body':'ตัวอย่างขั้นต่ำนี้ไม่ตรวจและไม่ต่อใหม่อัตโนมัติ ไม่วนกลับเข้า setup() เอง การทำงานรับส่งจึงอาจหยุดหลังหลุด หากต้องการระบบต่อใหม่ให้ดู mqtt_base ในหัวข้อ MQTT ที่ต้องใช้ ซึ่งเพิ่ม maintainConnection() ไว้ชัดเจน การ disconnect เมื่อ WiFi หลุดมีไว้ปิด connection เก่าฝั่งบอร์ด ไม่รับประกันว่า DISCONNECT ไปถึง Broker'},
 {'title':'แยกตรวจสามชั้นเมื่อไม่ทำงาน','body':'หนึ่ง: WiFi.status()==WL_CONNECTED และ localIP มีค่า สอง: mqtt.connect() สำเร็จด้วย broker/port/auth/client ID ที่ถูกต้อง สาม: subscribe สำเร็จและ Topic ตรงทุกตัวพิมพ์ พร้อมให้ผู้ส่งส่งค่าหลัง Subscribe การต่อ WiFi สำเร็จไม่รับประกันว่าถึง Broker และการต่อ Broker สำเร็จไม่รับประกันว่าเลือก Topic ถูก'},
 {'title':'ต้นทางกับส่วนที่ผู้จัดทำเว็บเพิ่ม','body':'สไลด์ 15 หน้า 64 ลิงก์ไป ObeOne-KMITL/lab_iot/arduino_R4/mqtt.ino ซึ่งใช้ WiFiS3 และ MQTTClient.h พร้อมลูปรอการเชื่อมต่อครั้งแรก หน้านี้เขียนตัวอย่างย่อใหม่เพื่ออธิบายแกนเดียวกัน ส่วนโค้ด maintainConnection() ในตัวอย่างอื่นเป็นส่วนที่เว็บเพิ่ม ไม่ใช่ฟังก์ชันจากไลบรารี โค้ดในหน้านี้ยังไม่ได้ยืนยัน compile และทดสอบบอร์ด/Broker จริง'},
],links=['wifi-minimum','mqtt-guide','mqtt-temp','seven','troubleshooting'],tips=['Arduino IDE: เลือก UNO R4 WiFi และติดตั้ง MQTT ของ Joel Gaehwiler ไม่ใช่ PubSubClient','ใช้ TCP port ที่อาจารย์กำหนด; WebSocket URL ที่ใช้ใน browser ไม่ใช่ค่าที่ใส่แทน BROKER/1883 โดยตรง','เปิด Serial Monitor 9600 แล้วดูว่าหยุดอยู่ขั้น WiFi connecting, MQTT connecting หรือ Subscribe failed'])

page('mqtt-guide','MQTT ที่ต้องใช้','MQTT','แนวคิด MQTT และตัวอย่างที่เพิ่มระบบต่อใหม่ maintainConnection()',codes=['mqtt_base'],lib=MQTT,links=['wifi-minimum','mqtt-minimum'],sections=[
 ['ภาพรวม','Publisher ส่งข้อความไป Topic ที่ Broker ส่วน Subscriber เลือก Topic ที่สนใจ บอร์ดหนึ่งเป็นได้ทั้งสองบทบาท ไม่ส่งตรงไปหา Client ID ของอีกเครื่อง'],
 ['ลำดับโค้ด','WiFi.begin → mqtt.begin(host,port,net) → onMessage(callback) → connect(uniqueID) → subscribe(topic) → loop() บ่อย ๆ → publish(topic,String(value))'],
 ['QoS','0: at most once อาจหาย ไม่มี ACK; 1: at least once อาจซ้ำ ต้องรับมือการทำงานซ้ำ; 2: exactly once ต่อการส่งมอบในโปรโตคอล มี handshake มากขึ้น ไม่ได้ทำให้ทุก action ในแอปไม่มีโอกาสซ้ำตลอดระบบ'],
 ['Retain','Broker เก็บค่าล่าสุดของ Topic และส่งให้ Subscriber ใหม่เมื่อ subscribe ใช้กับ state เช่นอุณหภูมิได้ ระวังคำสั่งเก่าถูกเรียกเมื่อเพิ่งเปิดบอร์ด การลบ retained message ส่ง payload ว่างแบบ retained'],
 ['Topic และ wildcard','ตัวพิมพ์เล็กใหญ่สำคัญ ใช้ / แบ่งระดับ + แทนหนึ่งระดับ, # แทนหลายระดับและอยู่ท้าย filter ใช้ wildcard ใน subscribe ไม่ใช้ใน publish ตั้ง prefix รหัสตนเองลดชนกับคนอื่น'],
 ['Client ID และ Keep Alive','Client ID ห้ามซ้ำ มิฉะนั้นอุปกรณ์เดิมอาจถูกตัด MQTT ต้องส่ง control packet หรือ PING ภายใน keep alive ฝั่ง broker จะตัดเมื่อเงียบเกินเกณฑ์ประมาณ 1.5 เท่า เรียก mqtt.loop() ต่อเนื่อง'],
 ['LWT','กำหนด will ก่อน connect: mqtt.setWill("physcom/YOUR_ID/status","offline",true,1); Broker ส่งเมื่อหลุดผิดปกติ เช่นไฟดับ/timeout ไม่ใช่เมื่อ disconnect ปกติ'],
 ['Session','MQTT 3.1.1 ก็มี persistent session ผ่าน Clean Session=false; MQTT 5 ใช้ Clean Start และ Session Expiry อย่าสับสนกับ retain สไลด์ระบุ session เฉพาะ MQTT 5 แต่ความสามารถเก็บ session มีมาก่อน'],
 ['API ของ 256dpi','publish(topic,payload,retained,qos), subscribe(topic,qos), onMessage(callback), connected(), lastError(), returnCode(), setCleanSession(false) ใช้ client ID เดิมเมื่อต้องการ session เดิม ตรวจขอบเขตการรองรับจากเวอร์ชันจริง'],
 ['TCP เทียบ WebSocket','UNO R4 ใช้ WiFiClient กับ MQTT TCP 1883 ในตัวอย่าง เว็บ browser ใช้ WebSocket path เช่น /mqtt และพอร์ต WS/WSS ของ Broker โดยเฉพาะ 8884 ในสไลด์เป็นค่าตัวอย่างของ Broker นั้น ไม่ใช่มาตรฐานทุก Broker'],
 ['ต่อใหม่และ callback','ตัวอย่างพยายาม WiFi เป็นช่วง ๆ แล้ว reconnect MQTT พร้อม subscribe ใหม่ หลีกเลี่ยง publish/subscribe ใน callback ของ 256dpi ให้เปลี่ยนตัวแปรแล้วทำต่อใน loop แทน'],
 ['ข้อจำกัดการสอบ','คอมคู่มือออฟไลน์ แต่ Arduino ต่อ Hotspot ส่ง Broker ได้ การติดตั้ง Library Manager และ board package บนคอมสอบขึ้นกับสิ่งที่ผู้จัดเตรียมไว้ ต้องตรวจล่วงหน้า']
],tips=['QoS ที่ส่งต่อถูกจำกัดด้วยระดับ publish และ subscription ที่ Broker ยอมรับ','โค้ดตัวอย่างใช้ MQTT 3.1.1 ตาม 256dpi/lwmqtt ไม่ใช่ MQTT 5','ใช้ Broker, authentication และพอร์ตตามโจทย์จริง ลิงก์ภายนอกเป็นอ้างอิงและเปิดไม่ได้เมื่อออฟไลน์'])
page('mqtt-sim','จำลอง MQTT','MQTT','ทดลอง Publish / Subscribe / Retain ในเครื่อง · ไม่เชื่อมบอร์ดจริง',tool='sim')
page('web-basics','HTML / CSS / JavaScript','เว็บ','พื้นฐานสำหรับคนลืมเนื้อหา พร้อมตัวอย่างที่แก้ได้',sections=[
 ['HTML: โครงสร้าง','<!doctype html> ระบุ HTML5, <html lang="th">, <head> ใส่ charset/meta/title/style, <body> ใส่เนื้อหา ปุ่มใช้ <button> ช่องกรอกใช้ <input> ข้อความจากบอร์ดใช้ <output> หรือ <span>'],
 ['id กับ class','id ต้องไม่ซ้ำ ใช้ document.getElementById("name") เพื่อหา element เฉพาะ class ใช้ซ้ำหลาย element และเลือกผ่าน .class ใน CSS'],
 ['CSS ที่ใช้บ่อย','selector { property: value; } เช่น .controls { display:flex; gap:12px; } ใช้ grid-template-columns:1fr 1fr สำหรับสองคอลัมน์ ใช้ @media เมื่อจอแคบ ระวัง width ล้นจอ'],
 ['JavaScript และ DOM','const ใช้ค่าที่ไม่ reassign, let ใช้ค่าที่เปลี่ยนได้; input.value เป็น string แปลงด้วย Number() และตรวจ Number.isFinite() อัปเดตข้อความด้วย textContent เพื่อลดการตีความ HTML จาก payload'],
 ['Event','button.addEventListener("click", handler) สำหรับปุ่ม; slider ใช้ input เพื่ออัปเดตทันที หรือ change เมื่อลากเสร็จ ใช้ function send(){...} หรือ () => {...}'],
 ['MQTT callback','เมื่อ connect สำเร็จจึง subscribe; เมื่อข้อความเข้าใช้ message.destinationName และ message.payloadString; แสดงสถานะ connect/failure/lost และอย่า send ก่อนเชื่อมต่อ'],
 ['String และ JSON','String(128) ได้ "128"; Number("25.54") ได้ 25.54; JSON.stringify({r:255,g:0,b:255}) เป็นข้อความ JSON; JSON.parse() ต้อง try/catch โค้ด Arduino ตัวอย่างใช้ Topic แยกสี จึงไม่ต้องเพิ่ม ArduinoJson'],
 ['Debug','เปิด DevTools → Console ดูข้อผิดพลาด ตรวจ id, วงเล็บ, ชื่อ function, path ไฟล์ JS และ Network สำหรับ WebSocket หน้า HTTPS ต้องใช้ WSS เพื่อไม่ติด mixed content'],
 ['ไฟล์ออฟไลน์','ใช้ไฟล์ JS ที่อยู่ในเครื่องแทน CDN ตัวอย่างดาวน์โหลดจากเว็บนี้ฝัง Paho ไว้แล้ว จึงไม่ต้องแนบ script แยก แต่ยังต้องมีเครือข่ายหากเลือกต่อ Broker จริง']
],codes=['web_starter'])
page('web-examples','เว็บควบคุมบอร์ด','เว็บ','เว็บตัวอย่างพร้อมดาวน์โหลด: ON/OFF, PWM, RGB และรับค่า Sensor',tool='web',links=['mqtt-web'])
page('calculators','ตัวคำนวณ','ตัวคำนวณ','เลือกสมการและดูการแทนค่าทีละขั้น',tool='calculators')
page('setup','ติดตั้ง / ตรวจไลบรารี','อุปกรณ์','ชื่อที่ต้องค้น ผู้พัฒนา และ API ให้ตรงกับตัวอย่าง',sections=[
 ['Board Manager','Arduino UNO R4 Boards — Arduino เลือกบอร์ด Arduino UNO R4 WiFi และพอร์ตที่ถูกต้อง ไม่ใช่ UNO R3/Minima สไลด์ 15 หน้า 69 เคยแนะนำ 1.2.1 สำหรับปัญหาในห้อง ไม่ใช่ข้อสรุปว่าทุกเวอร์ชันอื่นใช้ไม่ได้'],
 ['WiFiS3 / Wire / math.h',CORE+'; WiFiS3 และ Wire โดย Arduino มากับ core ส่วน math.h เป็น standard math header ไม่ต้องค้นติดตั้งไลบรารีชื่อ math'],
 ['MQTT',MQTT+' · ดาวน์โหลดต้นทาง https://github.com/256dpi/arduino-mqtt'],
 ['LiquidCrystal I2C',LCDLIB+' · ตรวจชื่อผู้พัฒนา Frank de Brabander ใน IDE และตัวอย่าง init() ให้ตรงกัน · upstream https://github.com/johnrickman/LiquidCrystal_I2C'],
 ['Keypad','ชุดนี้สแกนแถว–คอลัมน์เองตามสไลด์ จึงไม่ต้องติดตั้ง Keypad โดยคนอื่นเพิ่ม'],
 ['JavaScript MQTT','Paho MQTT JavaScript 1.1.0 — Eclipse Paho ฝังใน HTML ตัวอย่างแล้ว ใช้ Paho.Client / Paho.Message ในเวอร์ชันนี้ ไม่ใช่ Paho.MQTT.Client ของตัวอย่างเก่าบางชุด'],
 ['สถานะการตรวจ','เว็บและสูตรตรวจด้วยการทดสอบซอฟต์แวร์ รายการ compile แยกใน README/รายงานส่งมอบ ไม่อ้างว่าทดลองวงจรจริง ทุกวงจรต้องตรวจ pinout ของชิ้นส่วนที่ได้รับก่อนจ่ายไฟ']
])
page('reference-devices','อุปกรณ์ที่กล่าวถึงเพิ่มเติม','อุปกรณ์','ข้อมูลย่อจากสไลด์ ไม่ใช่ชุดโจทย์ปฏิบัติ',sections=[
 ['Flex sensor','ความต้านทานเปลี่ยนเมื่อโค้ง ใช้วงจรแบ่งแรงดันและ ADC ได้ แต่ต้องมีกราฟ/การสอบเทียบก่อนแปลงเป็นมุม'],
 ['Touch sensor','ตัวอย่างเซนเซอร์ความจุไฟฟ้า สัญญาณและแรงดันขึ้นกับโมดูล ไม่มีโค้ดทดลองเฉพาะในแลบที่ตรวจ'],
 ['Microphone / Piezoelectric','แปลงเสียงหรือการสั่นเป็นไฟฟ้า ไม่ถือว่าค่าดิบเป็น dB หรือแรงโดยไม่มีวงจรปรับสัญญาณและสอบเทียบ'],
 ['Solar cell / Speaker / Buzzer / Motor','ตัวอย่างการแปลงพลังงานในสไลด์ 14 หน้า 6 ไม่พบโจทย์ให้ต่อโดยตรง Motor ไม่ควรต่อขับจาก GPIO โดยตรง ต้องใช้ driver ที่เหมาะสม'],
 ['LED matrix บน UNO R4','สไลด์ชี้ตำแหน่ง matrix 12×8 บนบอร์ด ไม่พบโจทย์ควบคุมโดยตรงใน Lab 12–15'],
 ['Breadboard / Resistor','ตรวจแถวที่ต่อถึงกันและรางไฟที่อาจขาดกลาง ใช้ R 220/330Ω จำกัดกระแส LED และ R 10kΩ สำหรับ divider/pull-up ตามวงจร']
])
page('troubleshooting','ตรวจปัญหาและแปลงข้อมูล','MQTT','เช็กทีละชั้นจากสายไฟถึงเว็บ',sections=[
 ['ลำดับตรวจ','1. Board/port/upload → 2. LED หรือ Serial เดี่ยว → 3. Sensor → 4. LCD → 5. WiFi IP → 6. MQTT connect → 7. Topic/Payload → 8. เว็บ การเพิ่มทุกอย่างพร้อมกันทำให้แยกสาเหตุยาก'],
 ['ADC / PWM','R4 อ่านได้สูงสุด 14-bit แต่ค่าเริ่มต้น ADC 10-bit ตัวอย่างระบุ analogReadResolution(10); PWM ตัวอย่าง 8-bit จึงใช้ 0–255 อย่าใช้ 16383 หรือ 4095 แทน 1023 โดยไม่ตั้ง resolution ให้ตรง'],
 ['Integer division','ใช้ raw*5.0f/1023.0f เพื่อเก็บทศนิยม map() ใช้จำนวนเต็มและไม่ clamp เอง จึงใช้ constrain() เมื่อข้อมูลอาจเกินช่วง'],
 ['String / float','publish เป็นข้อความ: String(value,2); รับเลขทศนิยมด้วย toFloat() รับจำนวนเต็มด้วย toInt() แต่ toInt() อาจคืน 0 เมื่อข้อความไม่ใช่เลข จึงตรวจ payload ก่อนสั่งอุปกรณ์'],
 ['หลายงานและเวลา','ใช้ unsigned long now=millis(); if(now-last>=interval) {...} เพื่อรองรับ counter wrap หลีกเลี่ยง now>=last+interval และอย่า delay ยาวใน MQTT/Multi-LED/multiplex'],
 ['WiFi ไม่ติด','ตรวจ SSID/password รวมช่องว่าง Hotspot 2.4GHz ความเข้ากันได้โหมด security ระยะสัญญาณ และ WiFi.status() ดู localIP() หลังเชื่อมสำเร็จ'],
 ['MQTT ติดแล้วหลุด','Client ID ซ้ำหรือไม่ loop() ถูกเรียกบ่อยไหม มี code block/delay ยาวหรือเปล่า WiFi หลุดหรือ Broker ไม่ตอบ ตรวจ lastError()/returnCode() และ auth'],
 ['รับข้อความไม่ได้','Broker เดียวกัน Topic ตรงทุกตัวพิมพ์ slash และ prefix หรือไม่ subscribe หลัง connect/reconnect หรือยัง ลองส่ง payload ที่รู้ค่า เช่น "128" แยกจาก Sensor'],
 ['LCD มีไฟแต่ไม่แสดง','ตรวจ SDA=A4/SCL=A5, I2C address, contrast, library ผู้พัฒนา และ init() อย่าใช้ begin() ของอีก library โดยไม่ดู API'],
 ['เว็บเชื่อมไม่ได้','คอมออฟไลน์ต่อ public Broker ไม่ได้ ตรวจ WS/WSS, พอร์ตและ path ของ Broker ไม่ใช้ TCP 1883 ใน browser ตรวจ mixed content ใน Console']
])
page('sources','แหล่งอ้างอิงและสถานะ','MQTT','เอกสารต้นฉบับและข้อแก้ไขที่ต้องระวัง',tool='sources')

SKETCHES['web_starter']='''<!doctype html>
<html lang="th"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ทดลองปุ่ม</title>
<style>body{font-family:sans-serif;padding:24px} button{padding:12px}</style>
<button id="on">ON</button> <output id="value">0</output>
<script>
document.getElementById('on').addEventListener('click', () => {
  document.getElementById('value').textContent = '255';
  // Call MQTT publish after a successful connection.
});
</script></html>
'''

SOURCES=[
 ['โค้ด MQTT ที่สไลด์ 15 หน้า 64 อ้างอิง','https://github.com/ObeOne-KMITL/lab_iot/blob/main/arduino_R4/mqtt.ino'],
 ['Lab 12','https://github.com/TaeTanakrit0089/PhysicalComputing-167/tree/main/labs/labs12-IntroToMicrocontroller'],
 ['Lab 13','https://github.com/TaeTanakrit0089/PhysicalComputing-167/tree/main/labs/labs13-Digital_Read_and_Analog_Signal'],
 ['Lab 14','https://github.com/TaeTanakrit0089/PhysicalComputing-167/tree/main/labs/labs14-Sensor_and_LCD'],
 ['Lab 15','https://github.com/TaeTanakrit0089/PhysicalComputing-167/tree/main/labs/labs15-internet_of_things'],
 ['MQTT 256dpi และ API','https://github.com/256dpi/arduino-mqtt'],
 ['LCD library properties','https://github.com/johnrickman/LiquidCrystal_I2C/blob/master/library.properties'],
 ['Arduino UNO R4 WiFi','https://docs.arduino.cc/tutorials/uno-r4-wifi/cheat-sheet/'],
 ['Paho JavaScript API','https://eclipse.dev/paho/files/jsdoc/Paho.MQTT.Client.html'],
 ['MCP9700 datasheet','https://ww1.microchip.com/downloads/en/DeviceDoc/20001942G.pdf'],
 ['TTC05 Thermistor datasheet (ลิงก์ในสไลด์)','https://www.es.co.th/Schemetic/PDF/TTC05.PDF']
]

if __name__=='__main__':
    Path('work/physcom-src/content.json').write_text(json.dumps(dict(pages=PAGES,sketches=SKETCHES,sources=SOURCES),ensure_ascii=False),encoding='utf-8')
    print(len(PAGES),'pages;',len(SKETCHES),'code samples')
