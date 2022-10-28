/*
 * Program by Harsh Sharma at TI-CEPD Lab at NSUT
 * To be run on a Arduino/ Arduino compatible device with digital and Analog input pins and supporting 
 * Serial communication at 115200 baudrate
 * Also, Setup to acquire readings is required, to get more info refer to Science on a Stick experiment description
 * 
 * 3 input pins required, 1 analog and 2 digital
 * Analog pin is to read coil data
 * digital pins are used to trigger starting and stopping reading data
*/

#define pin1 A0       //Arduino analog pin to which coil is connected
#define pin2 4        //Arduino digital pin to which top trigger is connected
#define pin3 3        //Arduino digital pin to which bottom trigger is connected

//Pins for on-board LED
#define led_vcc 12
#define led_gnd 10


long int t1;          //variable to hold start time of readings

void setup(){
  
  //Serial initialized to 115200 baudrate, this matches with the value used by Data Acquisition program
  Serial.begin(115200);
  
  //Set analog pin as input for reading voltage induced through coil
  pinMode(pin1,INPUT);
  
  //Set digital pins as input for reading top and bottom trigger of the SoS apparatus
  pinMode(pin2,INPUT);
  pinMode(pin3,INPUT);
  
  //Set LED as Output 
  pinMode(led_vcc,OUTPUT);
  pinMode(led_gnd,OUTPUT);
  digitalWrite(led_vcc,HIGH);
  digitalWrite(led_gnd,LOW);
}
 
void loop(){
  
  //Wait until top trigger is triggered, after which coil data is read
  while(true){
    //When using hall effect sensor in pullup, change digitalRead(pin2) == LOW 
    //when using standard reed switch, change it to digitalRead(pin2) == HIGH
    if(digitalRead(pin2)==LOW){  //Top trigger hit condition
      t1=millis();                //Store current time as readings start time
      break;
    }
  }
  
  //Read coil data until bottom trigger is triggered
  while(true){
    if(digitalRead(pin3)==LOW){  //Bottom trigger hit condition
        for(int i=0;i<30;i++)
          Serial.println(analogRead(pin1));
          
        Serial.println("3000");   //Send End-Of-Data symbol

        //Send start and end time for readings
        Serial.println(t1);
        Serial.println(millis());
        break;    
      }
      else{
        Serial.println(analogRead(pin1));   //Continuously send data over Serial
      }
  }

  //delay between each reading
  delay(5000);
}
