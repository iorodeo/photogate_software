#include "system_state.h"
#include <Streaming.h>
#include <util/atomic.h>
#include "firmware.h"
#include "utility.h"

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
    Serial.begin(constants::BAUDRATE);

    // Setup photogates
    noInterrupts();
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        photogate_[i].setConfig(constants::PHOTOGATE_CONFIG[i]); 
        photogate_[i].initialize();
        int interruptNum = photogate_[i].getInterruptNum();
        attachInterrupt(interruptNum, onPinChangeFunc[i] ,CHANGE);
    }
    interrupts();

    // Setup reset pin
    pinMode(constants::RESET_PIN,INPUT_PULLUP);

    // Update
    reset();
    update();
}


void SystemState::reset()
{
    noInterrupts();
    startTime_ = micros();
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        photogate_[i].reset();
    }
    running_ = true;
    timeout_ = false;
    interrupts();
}

bool SystemState::isDone()
{
    bool done = true;
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        done &= photogate_[i].isDone(); 
    }
    return done;
}

void SystemState::update()
{
    checkOperatingMode();
    checkForResetButton();
    updatePhotogateLed();
    checkRunTime();
    checkForDone();
}


void SystemState::handleSerialRequest()
{
    while (Serial.available() > 0)
    {
        char cmd = Serial.read();
        switch (cmd)
        {
            case 'r':
                reset();
                break;

            case 'l':
                sendListData();
                break;

            case 'j':
                sendJsonData();
                break;

            case 'p':
                sendPrettyData();

            default:
                break;

        }
    }
}


void SystemState::sendListData()
{
    Serial << '[';
    Serial << running_ << ',';
    Serial << timeout_ << ',';
    Serial << operatingMode_ << ',';
    Serial << startTime_ << ',';
    Serial << getRunTime() << ',';
    for (int i=0; i < constants::NUMBER_OF_PHOTOGATES; i++)
    {
        photogate_[i].sendListData(startTime_);
        if (i < constants::NUMBER_OF_PHOTOGATES-1)
        {
            Serial << ',';
        }
    }
    Serial << ']';
}

void SystemState::sendJsonData()
{
    Serial << '{';
    Serial << "\"running\"" << ':' << boolToStr(running_);
    Serial << ",\"timeout\"" << ':' << boolToStr(timeout_);
    Serial << ",\"operatingMode\"" << ':' << getOperatingModeStr();
    Serial << ",\"startTime\"" << ':' << startTime_;
    Serial << ",\"runTime\"" << ':' << getRunTime();
    Serial << "[";
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        photogate_[i].sendJsonData(startTime_);
        if (i<constants::NUMBER_OF_PHOTOGATES-1)
        {
            Serial << ',';
        }
    }
    Serial << ']';
    Serial << '}' << endl;
}

void SystemState::sendPrettyData()
{
    Serial << "running:       " << running_ << endl;
    Serial << "timeout:       " << timeout_ << endl;
    Serial << "operatingMode: " << operatingMode_ << endl;
    Serial << "startTime:     " << startTime_ << endl;
    Serial << "runTime:       " <<  getRunTime() << endl;
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
    {
        Serial << "photogate: " << i << endl;
        photogate_[i].sendPrettyData(startTime_);
    }
    Serial << endl;
}


const char* SystemState::getOperatingModeStr()
{
    switch (operatingMode_)
    {
        case NO_PHOTOGATE:
            return "NO_PHOTOGATE";

        case ONE_PHOTOGATE:
            return "ONE_PHOTOGATE";

        case TWO_PHOTOGATE:
            return "TWO_PHOTOGATE";

        default:
            return "UNKNOWN";
    }
}


unsigned long SystemState::getRunTime()
{
    unsigned long runTime = 0;
    if (running_)
    {
        // Still running - runtime is elapsed time.
        unsigned long currTime = micros();
        runTime = currTime - startTime_;
    }
    else
    {
        if (!timeout_)
        {
            // No timeout - calculate runtime based on exit times.
            if (operatingMode_ == ONE_PHOTOGATE)
            {   
                // Runtime is exitTime - startTime for (only) connected photogate
                for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
                {
                    if (photogate_[i].isConnected())
                    {
                        runTime = photogate_[i].getExitTime(startTime_);
                        break;
                    }
                }
            }
            else if (operatingMode_ == TWO_PHOTOGATE)
            {
                // Runtime maximum over all photogate e.g. maximum (exitTime - startTime)
                for (int i=0; i<constants::NUMBER_OF_PHOTOGATES; i++)
                {
                    unsigned long runTimeTmp = photogate_[i].getExitTime(startTime_);
                    if (runTimeTmp > runTime)
                    {
                        runTime = runTimeTmp;
                    }
                }
            }
        } // if (!timeout)
        else
        {
            // We timed out - run time is maximum allowed runtime.
            runTime =  constants::MAXIMUM_RUNTIME;
        }
    }
    return runTime;
}


void SystemState::onPhotogatePinChange(int photogateNum)
{
    if (!running_)
    {
        return;
    }

    switch (operatingMode_)
    {
        case NO_PHOTOGATE:
            break;

        case ONE_PHOTOGATE:
            // Single phtotgate case always update
            photogate_[photogateNum].update();
            break;

        case TWO_PHOTOGATE:
            if (photogateNum == 0)
            {
                //Photogate 0 always updates
                photogate_[photogateNum].update();
            }
            else
            {
                // Photogate 1 update only if photoage 0 has registered an event 
                if (photogate_[0].getStateUnsafe() != Photogate::READY)
                {
                    photogate_[photogateNum].update();
                }
            }
            break;

        default:
            // Do nothing 
            break;
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
       reset(); // Is this what we want to do
   }
}


void SystemState::updatePhotogateLed()
{
    for (int i=0; i<constants::NUMBER_OF_PHOTOGATES;i++)
    {
        photogate_[i].setLedFromSignal();
    }
}


void SystemState::checkForResetButton()
{
    int resetPinValue = digitalRead(constants::RESET_PIN);
    if (resetPinValue == LOW)
    {
        reset();
    }
}

void  SystemState::checkRunTime()
{
    unsigned long runTime = getRunTime();
    if (runTime >= constants::MAXIMUM_RUNTIME)
    {
        ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
        {
            running_ = false;
            timeout_ = true;
        }
    } 
}


void SystemState::checkForDone()
{
    if (isDone())
    {
        running_ = false;
    }
}
