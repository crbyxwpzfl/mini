#include <Arduino.h>    // all this is arduino for an esp32    see following comments for how to compile with platformio    please tell me a one liner for these steps


// find board with 'pio boards adafruit_qt'    and init pio with eg 'pio project init -b adafruit_qtpy_esp32s3_n4r2    then gather libraries with see blowus'
#include <WiFiManager.h>   // pio pkg install -l https://github.com/tzapu/WiFiManager.git
#include <TelnetStream.h>   // pio pkg install -l https://github.com/JAndrassy/TelnetStream.git
// finaly move this to ./src/main.cpp and compile with 'pio run'


void setup() {
    // WiFi.mode(WIFI_STA); // explicitly set mode, esp defaults to STA+AP
    // it is a good practice to make sure your code sets wifi mode how you want it.

    // put your setup code here, to run once:
    Serial.begin(115200);
    
    //WiFiManager, Local intialization. Once its business is done, there is no need to keep it around
    WiFiManager wm;

    // reset settings - wipe stored credentials for testing
    // these are stored by the esp library
    //wm.resetSettings();

    // Automatically connect using saved credentials,
    // if connection fails, it starts an access point with the specified name ( "AutoConnectAP"),
    // if empty will auto generate SSID, if password is blank it will be anonymous AP (wm.autoConnect())
    // then goes into a blocking loop awaiting configuration and will return success result

    bool res;
    // res = wm.autoConnect(); // auto generated AP name from chipid
    res = wm.autoConnect("AutoConnectAP"); // anonymous ap
    // res = wm.autoConnect("AutoConnectAP","password"); // password protected ap

    if(!res) {
        Serial.println("Failed to connect");
        // ESP.restart();
    } 
    else {
        //if you get here you have connected to the WiFi    
        Serial.println("connected...yeey :)");
    }


    TelnetStream.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  static unsigned long next;
  if (millis() - next > 5000) {
    next = millis();
    TelnetStream.println("hallo wie geths");
  }
}
