
const int c = 261, a = 440;			// Tones used for alarm speaker
const int speakerPin = 0;			// Output pin sending signal to speaker		
const int trigPin = 4;				// Trigger Output Pin for Ultrasonic Sensor
const int echoPin = 5;				// Echo Input Pin for Ultrasonic Sensor
int sensorDistance = 0;				// Initalize distance used for calculating distance
int sensorDuration = 0;				// Initialize duration used for calculating distance
int counter = 0; 					//counter is used to keep track of what tone is playing
									

#define accelerationThreshold 50    // When acceleration change goes beyond this threshold, the alarm will be triggered.

AccelerationReading previousAccel;	// Variale which will hold previous acclerometer readings
int sound[6] = {a,c,a,c,a,c};		// An array of the two tones going back and forth as the alarm has been triggered

void setup()
{

pinMode(trigPin, OUTPUT);			// Setting pins to input/outputs
pinMode(echoPin, INPUT);
pinMode(speakerPin, OUTPUT);

  previousAccel = Bean.getAcceleration(); 		// Initial acceleration reading

}

void loop()

{

	// Get the current acceleration with a conversion of 3.91×10-3 g/unit.
  AccelerationReading currentAccel = Bean.getAcceleration();   
  
  // Find the difference between the current acceleration and that of 200ms ago.
  int accelDifference = getAccelDifference(previousAccel, currentAccel);  

  // Update previous Accel for the next loop. 
  previousAccel = currentAccel;   

  digitalWrite(trigPin,LOW);					// Start sensor trigger pin with a LOW voltage

delayMicroseconds(2);							// Short delay before setting trigger pin HIGH voltage

digitalWrite(trigPin,HIGH);						// Set trigger pin for sensor HIGH

  delayMicroseconds(10);						// Delay between HIGH and LOW sensor voltages				

  digitalWrite(trigPin,LOW);					// Set trigger pin for sensor LOW 

  sensorDuration = pulseIn(echoPin,HIGH);		// Calculate time sensor took for pulse to respond	

  sensorDistance = (sensorDuration/2) / 29.1;	// Calculate distance in cm

  

  Bean.setLed(255,0,0);

    // Check if the alarm has been reached our threshold  or if sensor detect object to trigger alarm

 if(sensorDistance < 25 || accelDifference > accelerationThreshold){

    //Turn LED of bean to Blue showing alarm has been triggered

  Bean.setLed(0,0,255);

    

    //tones[counter] = the tone that needs to be played and tones[counter+1] = the duration

    alarmTrig(sound[counter],300);  

    

    if(counter>5){

      //Reset the counter when it as reached the end of the tones array

      counter=0; 

    }

    else{

      counter+=1;

    }

  Bean.sleep(25);

  }

  else{ 

   // If the alarm is off, turn off the LED

   

   Bean.setLed(0,0,0);

    Bean.sleep(200);

  }

}

//This function plays the tones on the speaker

void alarmTrig(int note, int duration)

{

  //If note==0 no tone should be played

  if(note==0){

    delay(duration);

  }

  else{

    //Play tone on speaker pin

    tone(speakerPin, note, duration); 

    delay(duration);

    //Stop tone on speaker pin

    noTone(speakerPin);

     

  }

}

// This function calculates the difference between two acceleration readings

int getAccelDifference(AccelerationReading readingOne, AccelerationReading readingTwo){

  int deltaX = abs(readingTwo.xAxis - readingOne.xAxis);

  int deltaY = abs(readingTwo.yAxis - readingOne.yAxis);

  int deltaZ = abs(readingTwo.zAxis - readingOne.zAxis);

  // Return the magnitude

  return deltaX + deltaY + deltaZ;   

}
