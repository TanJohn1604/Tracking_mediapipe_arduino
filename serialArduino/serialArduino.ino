#define numOfValsRec 2
#define digitsPerValRec 3
#include <Servo.h>

int valsRec[numOfValsRec];
int stringLength=numOfValsRec*digitsPerValRec+1;
int counter =0;
bool counterStart=false;
String receivedString;
int prepan=90;
int pretilt=90;
Servo pan; 

Servo tilt;

void setup() {
        Serial.begin(9600);     // mở serial với baudrate 9600
        pinMode(LED_BUILTIN, OUTPUT);
        tilt.attach(9);
        pan.attach(10);
        valsRec[0]=90;
valsRec[1]=90;
}

void receiveData(){
  while (Serial.available()){
    char c = Serial.read();
    if (c=='$'){
      counterStart=true;
    }
    if (counterStart){
      if(counter<stringLength){
        receivedString=String(receivedString+c);
      counter++;
      }
      if(counter>=stringLength){
       for (int i=0;i<numOfValsRec;i++){
        int num=(i*digitsPerValRec)+1;
        valsRec[i]=receivedString.substring(num,num+digitsPerValRec).toInt();
       }
       receivedString="";
       counter=0;
       counterStart=false;
      }
    }
    
  }
}

void serpan(int prepos,int despos){

if(despos>prepos){

for(int pos=prepos; pos<=despos;pos+=1){
  pan.write(pos);   
    delay(15); 
}
}
else{
  for(int pos=prepos; pos>=despos;pos-=1){
  pan.write(pos);   
    delay(15); 
}
}
}

void sertilt(int prepos,int despos){

if(despos>prepos){

for(int pos=prepos; pos<=despos;pos+=1){
  tilt.write(pos);   
    delay(15); 
}
}
else{
  for(int pos=prepos; pos>=despos;pos-=1){
  tilt.write(pos);   
    delay(15); 
}
}
}
void loop() {
  
receiveData();
        // nếu còn có thể đọc được 
//        
//
//        pan.write(valsRec[0]);
//      
//        tilt.write(valsRec[1]);


serpan(prepan,valsRec[0]);
prepan=valsRec[0];
delay(15);
sertilt(pretilt,valsRec[1]);
pretilt=valsRec[1];
delay(15);

//delay(15);
//tilt.write(valsRec[1]);  


//delay(15);
//pan.write(90); 
//delay(15);
//tilt.write(90);          
}
