#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
//#include <ESP8266mDNS.h>
IPAddress ip( 192, 168, 2, 206 );
IPAddress gateway( 192, 168, 2, 1 );
IPAddress subnet( 255, 255, 255, 0 );

#ifndef STASSID
// #define STASSID "Zet_SH256_RTS_Wi-Fi5"
// #define STAPSK "58469989"
#define STASSID "ALF-KAI.RU"
#define STAPSK "knitukai"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;


const String security_key = "tsVPw1T7PoQSP%2B9gbgrhT4RFchMzK8EQfa9cwuINuDEArAzX6YTbk7LijfeFnzwbDh%2FQtMxKXmnoknwz6RF%2BTw";

ESP8266WebServer server(80);

const int led = LED_BUILTIN;

const String postForms = "<html>\
  <head>\
    <title>ESP8266 Web Server POST handling</title>\
  </head>\
  <body>\
    <form method=\"post\" enctype=\"application/json\" action=\"/postform/\">\
      <input type=\"text\" name=\"secret_key\"><br>\
      <input type=\"submit\" value=\"Submit\">\
    </form>\
  </body>\
</html>";


#define tx433Pin D4
#define MAX_DELTA 200
#define Pe 413
#define Pe2 Pe*2

void handlePostForm()
{
  if (server.method() != HTTP_POST)
  {
    server.send(405, "text/plain", "Method Not Allowed");
  }
  else
  {
    digitalWrite(led, 1);
    Serial.println("ArgName: " + server.argName(1) + " | Arg: " + server.arg("secret_key"));
    if (server.arg("secret_key").equals(security_key)) {
      OpenANMotors();
      server.send(200, "application/json", "{\"value\": \"1\"}");
      
    }
    else
      server.send(200, "application/json", "{\"value\": \"0\"}");
    digitalWrite(led, 0);
  }
}

void handleRoot()
{
  server.send(200, "text/html", postForms);
}

// Transmitter Codes
//-----------------------------------------
void SendBit(byte b) {
  if (b == 0) {
    digitalWrite(tx433Pin, HIGH); // 0
    delayMicroseconds(Pe2);
    digitalWrite(tx433Pin, LOW);
    delayMicroseconds(Pe);
  }
  else {
    digitalWrite(tx433Pin, HIGH); // 1
    delayMicroseconds(Pe);
    digitalWrite(tx433Pin, LOW);
    delayMicroseconds(Pe2);
  }
}
void SendANMotors(long c1, long c2)
{

  for (int j = 0; j < 4; j++)
  {
    // отправляем 12 начальных импульсов 0-1
    for (int i = 0; i < 12; i++) {
      delayMicroseconds(Pe);
      digitalWrite(tx433Pin, HIGH);
      delayMicroseconds(Pe);
      digitalWrite(tx433Pin, LOW);
    }
    delayMicroseconds(Pe * 10);
    // отправляем первую половину
    for (int i = 4 * 8; i > 0; i--) {
      digitalWrite(led, HIGH);
      SendBit(bitRead(c1, i - 1));
      digitalWrite(led, LOW);
    }
    // вторую половину
    for (int i = 4 * 8; i > 0; i--) {
      digitalWrite(led, HIGH);
      SendBit(bitRead(c2, i - 1));
      digitalWrite(led, LOW);
    }
    // и еще пару ненужных бит, которые означают батарейку и флаг повтора
    SendBit(1);
    SendBit(1);
    delayMicroseconds(Pe * 39);
  }
}
void OpenANMotors() {
  long c1 = 0x20240000 + 0x101 * random(0xff); // AN-MOTORS хотят рандом - получит рандом ))
  long c2 = 0x6A19BE24;
  SendANMotors(c1, c2);
}

void setup()
{
  pinMode(tx433Pin, OUTPUT);

  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  WiFi.config(ip, gateway, subnet);
  Serial.println("Connecting to WiFi");

  // while(WiFi.status() != WL_CONNECTED)
  while (!WiFi.isConnected())
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

//  if (MDNS.begin("esp8266")) 
//    Serial.println("MDNS responder started!");

  server.on("/", handleRoot);
  server.on("/postform/", handlePostForm);

  server.begin();
  Serial.println("HTTP server started");
}

void loop()
{
  server.handleClient();
}
