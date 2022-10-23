#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
//#include <ESP8266mDNS.h>
IPAddress ip( 192, 168, 2, 187 );
IPAddress gateway( 192, 168, 2, 1 );
IPAddress subnet( 255, 255, 255, 0 );

#ifndef STASSID
#define STASSID "ALF-KAI.RU"
#define STAPSK "knitukai"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

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

void handlePostForm()
{
  if (server.method() != HTTP_POST)
  {
    digitalWrite(led, 1);
    server.send(405, "text/plain", "Method Not Allowed");
    digitalWrite(led, 0);  
  }
  else
  {
    String security_key = "tsVPw1T7PoQSP%2B9gbgrhT4RFchMzK8EQfa9cwuINuDEArAzX6YTbk7LijfeFnzwbDh%2FQtMxKXmnoknwz6RF%2BTw";
    digitalWrite(led, 1);
    
    Serial.println("ArgName: " + server.argName(1) + " | Arg: " + server.arg("secret_key"));
    if (server.arg("secret_key").equals(security_key))
      server.send(200, "application/json", "{\"value\": \"1\"}");
    else
      server.send(200, "application/json", "{\"value\": \"0\"}");
    digitalWrite(led, 0);
  }
}

void handleRoot()
{
  digitalWrite(led, 1);
  server.send(200, "text/html", postForms);
  digitalWrite(led, 0);
}

void setup()
{
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  WiFi.config(ip, gateway, subnet);
  Serial.println("Connecting to WiFi");

  while(WiFi.status() != WL_CONNECTED)
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
