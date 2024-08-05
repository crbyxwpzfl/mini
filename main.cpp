#include <Arduino.h>    // all this is arduino for an esp32    see following comments for how to compile with platformio    please tell me a one liner for these steps


//  not jet working for some reason to build a diferent file system for eg spiffs or littlefs
//  platformio run --target buildfs --environment adafruit_qtpy_esp32s3_n4r2
//  platformio run --target uploadfs --environment adafruit_qtpy_esp32s3_n4r2
//#include <SPIFFS.h>
// likley preferences is enough for me



// read current partion table on esp32 https://iot.stackexchange.com/questions/4287
// gather esptool.py with 'pip install esptool' and gen_esp32part.py from https://github.com/espressif/arduino-esp32.git
// 'esptool.py read_flash 0x9000 0xc00 ptable.img' or 0x8000 for older systems
// 'gen_esp32part.py ptable.img' prints out partion table



// find board with 'pio boards adafruit_qt'    and init pio with eg 'pio project init -b adafruit_qtpy_esp32s3_n4r2    then gather libraries with see blowus'

#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <MycilaWebSerial.h>  // pio pkg install -l https://github.com/mathieucarbou/MycilaWebSerial.git
//#include <WebSerialLite.h>  // pio pkg install -l https://github.com/asjdf/WebSerialLite.git


// finaly move this to ./src/main.cpp and compile with 'pio run'


AsyncWebServer server(80);

const char* ssid = "Multiversum R"; // Your WiFi SSID
const char* password = "Lines+lin55"; // Your WiFi Password


/* Message callback of WebSerial */
void recvMsg(uint8_t *data, size_t len){
  WebSerial.println("Received Data...");
  String d = "";
  for(int i=0; i < len; i++){
    d += char(data[i]);
  }
  WebSerial.println(d);
  Serial.println(d);
}

void setup() {
    Serial.begin(115200);
    Serial.print("hallo");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.printf("WiFi Failed!\n");
        return;
    }
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    // WebSerial is accessible at "<IP Address>/webserial" in browser
    WebSerial.begin(&server);
    /* Attach Message Callback */
    WebSerial.onMessage(recvMsg);
    server.begin();
}

void loop() {
    delay(2000);
    Serial.println("hallo");
    // we suggest you to use `print + "\n"` instead of `println`
    // because the println will send "\n" separately, which means
    // it will cost a sending buffer just for storage "\n". (there
    // only 8 buffer space in ESPAsyncWebServer by default)
    WebSerial.print(F("IP address: "));
    // if not use toString the ip will be sent in 7 part,
    // which means it will cost 7 sending buffer.
    WebSerial.println(WiFi.localIP().toString());
    WebSerial.printf("Millis=%lu\n", millis());
    WebSerial.printf("Free heap=[%u]\n", ESP.getFreeHeap());
}
