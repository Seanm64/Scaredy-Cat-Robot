#include<Servo.h>
#include<FastLED.h>

#define NUM_LEDS 8
#define LED_PIN 6
Servo left;
Servo right;

CRGB led[NUM_LEDS];
String serialData;

void setup() {
  // put your setup code here, to run once:
  left.attach(10);
  right.attach(11);
  Serial.begin(9600);
  Serial.setTimeout(10);

  FastLED.addLeds<NEOPIXEL, LED_PIN>(led, NUM_LEDS);

  //Literally just a cool fade in effect, no reason for it here :)
  fadeIntoBlue();

}

void loop() {
  // put your main code here, to run repeatedly:

}



void serialEvent()
{
  serialData = Serial.readString();
  //Serial.print(serialData);
  if (serialData == "a")
  {
    freakout();
  }

  if (serialData == "b") //For testing purposes
  {
    testLEDs();
  }
}


//Checks data to make sure it's valid and SHOULD freak out
boolean serialConfirm(String data)
{

  return true;
}

//Moves motors, changes LEDs
void freakout()
{
  //Instantly turns LEDs red
  for (int i = 0; i < NUM_LEDS; i = i + 1)
  {
    led[i] = CRGB(255, 0, 0);//red
    FastLED.show();
  }

  //Shimmies the motors
  left.write(60);
  delay(250);
  right.write(120);
  delay(250);
  left.write(90);
  delay(250);
  left.write(60);
  delay(500);
  right.write(90);
  left.write(90);

  calmDown();
}

//Executes after it's done freaking out
void calmDown()
{
  //Stops the motors
  left.write(90);
  right.write(90);

  fadeIntoBlue();
}


void fadeIntoBlue() //From red to blue
{
  for (int fade = 180; fade > 0; fade = fade - 1)
  {
    for (int i = 0; i < NUM_LEDS; i = i + 1)
    {
      led[i] = CRGB(fade, 0, 0);//fades down from red
      FastLED.show();
    }
    delay(3);
  }


  for (int fade = 0; fade < 255; fade = fade + 1)
  {
    for (int i = 0; i < NUM_LEDS; i = i + 1)
    {
      led[i] = CRGB(0, 0, fade); //blue
    }
    FastLED.show();
  }
  delay(3);
}


void testLEDs()
{
  for (int fade = 255; fade > 0; fade = fade - 1)
  {
    for (int i = 0; i < NUM_LEDS; i = i + 1)
    {
      led[i] = CRGB(0, fade, 0);//fades down from green
      FastLED.show();
    }
    delay(3);
  }


  for (int fade = 0; fade < 255; fade = fade + 1)
  {
    for (int i = 0; i < NUM_LEDS; i = i + 1)
    {
      led[i] = CRGB(0, 0, fade);//fade back to blue
    }
    FastLED.show();
  }
  delay(3);


}
