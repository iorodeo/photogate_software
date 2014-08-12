#include <Streaming.h>
#include "photogate.h"
#include "constants.h"

Photogate photogate[constants::NUM_PHOTOGATE];

void interruptTest()
{
    static bool state = true;
    if (state == true)
    {
        digitalWrite(photogate[0].getLedPin(),LOW);
        state = false;
    }
    else
    {
        digitalWrite(photogate[0].getLedPin(),HIGH);
        state = true;
    }

}

void setup()
{
    Serial.begin(115200);

    for (int i=0; i<constants::NUM_PHOTOGATE; i++)
    {
        photogate[i].setConfig(constants::PHOTOGATE_CONFIG[i]); 
        photogate[i].initialize();
        attachInterrupt(photogate[i].getInterruptNum(), interruptTest ,CHANGE);
        photogate[i].printConfig();
        Serial << endl;
    }
    interrupts();
}

void loop()
{
    for (int i=0; i<constants::NUM_PHOTOGATE; i++)
    {
        Serial << "photogate[" << i <<"].isConnected = " << photogate[i].isConnected() << endl;
    }
    Serial << endl;
    delay(200);
}
