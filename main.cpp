#include <Arduino.h>
#include <Wire.h>
#include <NeoPixelBus.h>
#include <Arduino_LSM6DS3.h>
#include <math.h>

const int rings[] = {8, 12, 16, 20, 24, 24, 24, 20, 16, 12, 8, 1};
int maxbrightness = 5;
const int numled = 186;
const int range = 30;
int state = 1;
int wait = 100;
int dlay = 0;
NeoPixelBus<NeoGrbwFeature, Neo800KbpsMethod> led(numled, 6);

RgbwColor white(0,0,0,maxbrightness);
RgbwColor red(maxbrightness,20,0,0);
RgbwColor green(0,maxbrightness,0,0);
RgbwColor blue(0,0,maxbrightness,0);
RgbwColor all(maxbrightness,maxbrightness,maxbrightness,maxbrightness);
RgbwColor black(0);

//create led adress location table.  Data is in the order of (adress, theta, phi)
int ledlocation[numled*3];

void setup() {
  Serial.begin(115200);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  int temp = 0;
  //set adresses
  for( int a = 0; a < numled; a++){
    ledlocation[temp] = a;
    temp = temp+3;
  }

  //set theta around y axis
  temp = 1;
  for(int a = 0; a < 12; a++){
    float x = 360.0/rings[a];
    for(int t = 1; t <= rings[a]; t++){
      ledlocation[temp] = x*t;
      temp=temp+3;
    }

  }

  //set phi
  temp = 2;
  for(int a = 0; a < 13; a++){
    for(int t = 0; t < rings[a]; t++){
      ledlocation[temp] = 15*a;
      temp=temp+3;
    }
  }

  //print the adress table
  for(int i = 0; i < numled*3; i+=3){
    Serial.print(ledlocation[i]);
    Serial.print(", ");
    Serial.print(ledlocation[i+1]);
    Serial.print(", ");
    Serial.println(ledlocation[i+2]);
  }

  led.Begin();
  led.Show();
}

void loop() {
  
  float Gx, Gy, Gz;
  IMU.readGyroscope(Gx, Gy, Gz);
  Serial.println(Gx);
  Serial.println(state);
  Serial.println(wait);

  if(wait >= 10){
    if(Gx >= 1000.0){
      state+=1;
      Serial.println("here");
      wait = 0;
      if(state > 4){
        state = 1;
      }
    }
  }
  else{
    wait++;

  }


  if(state == 1){
  for(int t = 0; t<=numled; t++){
  led.SetPixelColor(t, white);
  }
  led.Show();
 
  }
  //flash all leds on and off
  /*if(state == 1){
  for(int t = 0; t<=numled; t++){
  led.SetPixelColor(t, white);
  }
  led.Show();
  dlay++;
  }
  }
  else if(dlay >= 0){
  for(int t = 0; t<=numled; t++){
  led.SetPixelColor(t, black);
  }
  led.Show();
  dlay--;
  }/*
  for(int i = 0; i < numled*3; i+=3){
    Serial.print("1");
    Serial.print(", ");
    Serial.print(ledlocation[i+1]);
    Serial.print(", ");
    Serial.println(ledlocation[i+2]);
  }
  }*/



  //accelerometer data input
  else if(state ==2){
  float Ax, Ay, Az;
  float theta;
  float phi;
  
    if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(Az, Ax, Ay);
  }
  theta = (57.295* atan2(Ay,Ax))+180;
  phi = (57.295*atan2(sqrt((Ax*Ax)+(Ay*Ay)),Az));


  /*Serial.print(Ax);
  Serial.print("  ");
  Serial.print(Ay);
  Serial.print("  ");
  Serial.println(Az);
  Serial.print(theta);
  Serial.print("  ");
  Serial.println(phi);*/


  //look at theta
    for(int w = 1; w < numled*3; w = w+3){
      int checktheta = ledlocation[w]+70;
      int checkphi = ledlocation[w+1];
      if(checktheta >= theta-range && checktheta <= theta+range && checkphi >= phi-range && checkphi <= phi+range){
        led.SetPixelColor(ledlocation[w-1],white);
        //Serial.println(ledlocation[w-1]);
      
      }
      else{
        led.SetPixelColor(ledlocation[w-1], black);
     
      }
    
    }
    led.Show();
    delay(0);
  }




  //rotating oange and green lights
  else if(state == 3){
    Serial.println("here");
  for(int t = 0; t <= 360; t+=5){
  for(int w = 1; w < numled*3; w = w+3){
    int checktheta = ledlocation[w];
    if(checktheta >= t-20 && checktheta <= t+20){
      led.SetPixelColor(ledlocation[w-1], red);
      //Serial.println(ledlocation[w-1]);
      
    }
    else if(checktheta >= t+160 && checktheta <= t+200){
      led.SetPixelColor(ledlocation[w-1], green);
    }
    else if(checktheta >= t+340 || checktheta <= t-340){
      led.SetPixelColor(ledlocation[w-1], red);
      
    }
    else if(checktheta >= t-190 && checktheta <= t-160){
      led.SetPixelColor(ledlocation[w-1], green);
    }
    else{
      led.SetPixelColor(ledlocation[w-1], black);
     
    }
    
  }
  led.Show();
  }
  }



//rotating white light
  else if(state == 4){
  for(int t = 0; t <= 360; t+=5){
  for(int w = 1; w < numled*3; w = w+3){
    int checktheta = ledlocation[w];
    int checkphi = ledlocation[w+1];
    if(checktheta >= t-20 && checktheta <= t+20){
      led.SetPixelColor(ledlocation[w-1], white);
      
    }
    else if(checktheta >= t+340 || checktheta <= t-340){
      led.SetPixelColor(ledlocation[w-1], white);
      
    }
    else{
      led.SetPixelColor(ledlocation[w-1], black);
     
    }
    
  }
  led.Show();
  delay(0);
  }
  }

}