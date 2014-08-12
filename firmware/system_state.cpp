#include "system_state.h"
#include <Streaming.h>
#include "firmware.h"

void (*onPinChangeFunc[constants::NUMBER_OF_PHOTOGATES])() = 
{
    onPhotogatePinChange0,
    onPhotogatePinChange1
};


// SystemState Public Methods
// ----------------------------------------------------------------------------

SystemState::SystemState() {}


void SystemState::initialize()
{
    // Setup photogates
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        photogate_[i].setConfig(constants::PHOTOGATE_CONFIG[i]); 
        photogate_[i].initialize();
        int interruptNum = photogate_[i].getInterruptNum();
        attachInterrupt(interruptNum, onPinChangeFunc[i] ,CHANGE);
    }

    // Setup reset pin
    pinMode(constants::RESET_PIN,INPUT_PULLUP);

    // Reset time counter and enable interrtups
    update();
    reset();
    interrupts();
}


void SystemState::reset()
{
    startTime_ = micros();
}


void SystemState::update()
{
    checkOperatingMode();
    checkForResetButton();
    updatePhotogateLed();


    Serial << "startTime:     " << startTime_ << endl;
    Serial << "operatingMode: " << operatingMode_ << endl;
    Serial << "sig 0:         " << photogate_[0].getSignal() << endl;
    Serial << "sig 1:         " << photogate_[1].getSignal() << endl;
    Serial << endl;
}


void SystemState::onPhotogatePinChange(int photogateNum)
{
    static bool state[constants::NUMBER_OF_PHOTOGATES] = {0,0};

    if (photogateNum >= constants::NUMBER_OF_PHOTOGATES)
    {
        return;
    }

    if (state[photogateNum] == true)
    {
        photogate_[photogateNum].setLedOff();
        state[photogateNum] = false;
    }
    else
    {
        photogate_[photogateNum].setLedOn();
        state[photogateNum] = true;
    }


}

// SystemState Protected Methods
// ----------------------------------------------------------------------------


void SystemState::checkOperatingMode()
{
    //  Get number of connected photogates
    int numConnected = 0;
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        if (photogate_[i].isConnected())
        {
            numConnected++;
        }
    }

   //Get operating mode based on number of connected photogates
   OperatingMode mode;
   switch (numConnected)
   {
       case 0:
           mode = NO_PHOTOGATE;
           break;

       case 1:
           mode = ONE_PHOTOGATE;
           break;

       case 2:
           mode = TWO_PHOTOGATE;
           break;
   }

   // If mode change - 
   if (mode != operatingMode_)
   {
       operatingMode_ = mode;
   }
}


void SystemState::updatePhotogateLed()
{
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES;i++)
    {
        if (photogate_[i].isConnected())
        {

        }
    }
}


void SystemState::checkForResetButton()
{
    int resetPinValue = digitalRead(constants::RESET_PIN);
    if (resetPinValue == LOW)
    {
        startTime_ = micros();
    }
}

