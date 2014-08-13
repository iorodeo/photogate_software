#include "photogate.h"
#include <util/atomic.h>
#include <Streaming.h>
#include "utility.h"

// Photogate Public Methods
// ----------------------------------------------------------------------------

Photogate::Photogate(PhotogateConfig config)
{
    setConfig(config);
    initFlag_ = false;
}


void Photogate::initialize()
{
    pinMode(config_.ledPin,OUTPUT);
    pinMode(config_.signalPin,INPUT);
    pinMode(config_.autoDetectPin,INPUT_PULLUP);
    digitalWrite(config_.ledPin,HIGH);
    initFlag_ = true;
    reset();
};


bool Photogate::isInitialized()
{
    return initFlag_;
}


void Photogate::reset()
{
    state_ =  READY;
    entryTime_ = 0;
    exitTime_ = 0;
}


PhotogateConfig Photogate::getConfig()
{
    return config_;
}

void Photogate::setConfig(PhotogateConfig config)
{
    config_ = config;
    setAllBitMaskAndPort();
}


void Photogate::printConfig()
{
    Serial << "ledPin         = " << config_.ledPin << endl;
    Serial << "signalPin      = " << config_.signalPin << endl;
    Serial << "autoDetectPin  = " << config_.autoDetectPin << endl;
    Serial << "interruptNum   = " << config_.interruptNum << endl;
}


int Photogate::getLedPin()
{
    return config_.ledPin;
}


void Photogate::setLedPin(int pinNum)
{
    config_.ledPin =  pinNum;
    setLedBitMaskAndPort();
}


int Photogate::getSignalPin()
{
    return config_.signalPin;
}

void Photogate::setSignalPin(int pinNum)
{
    config_.signalPin = pinNum;
    setSignalBitMaskAndPort();
}


int Photogate::getAutoDetectPin()
{
    return config_.autoDetectPin;
}


void Photogate::setAutoDetectPin(int pinNum)
{
    config_.autoDetectPin = pinNum;
    setAutoDetectBitMaskAndPort();
}


int Photogate::getInterruptNum()
{
    return config_.interruptNum;
}


unsigned long  Photogate::getEntryTime()
{
    unsigned long entryTimeCpy;
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
    {
        entryTimeCpy = entryTime_;
    }
    return entryTimeCpy;
}


unsigned long  Photogate::getExitTime()
{
    unsigned long exitTimeCpy;
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
    {
        exitTimeCpy = exitTime_;
    }

    return exitTimeCpy;
}


Photogate::State Photogate::getState()
{
    State stateCpy;
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
    {
        stateCpy = state_;
    }
    return stateCpy;
}


bool Photogate::hasEntryTime()
{
    if (getState() != READY)
    {
        return true;
    }
    else
    {
        return false;
    }
}


bool Photogate::hasExitTime()
{
    if (getState() == DONE)
    {
        return true;
    }
    else
    {
        return false;
    }
}


bool Photogate::isDone()
{
    if (state_ == DONE)
    {
        return true;
    }
    else
    {
        return false;
    }
}


void Photogate::sendListData()
{
    Serial << getState() << ',';
    Serial << hasEntryTime() << ',';
    Serial << getEntryTime() << ',';
    Serial << hasExitTime() << ',';
    Serial << getExitTime() << ',';
    Serial << isDone();
}


void Photogate::sendJsonData()
{
    Serial << '{';
    Serial << "\"state\"" << ':' << getStateStr();
    Serial << ",\"isConnected\"" << ':' << boolToStr(isConnected());
    Serial << ",\"hasEntryTime\"" << ':' << boolToStr(hasEntryTime());
    Serial << ",\"entryTime\"" << ':' << entryTime_;
    Serial << ",\"hasExitTime\"" << ':' << boolToStr(hasExitTime());
    Serial << ",\"exitTime\"" << ':' << exitTime_ << endl;
    Serial << ",\"isDone\"" << ':' << boolToStr(isDone());
    Serial << '}';
}


void Photogate::sendPrettyData()
{
    Serial << "  state:        " << getState() << endl;
    Serial << "  hasEntryTime: " << hasEntryTime() << endl;
    Serial << "  entryTime:    " << getEntryTime() << endl;
    Serial << "  hasExitTime:  " << hasExitTime() << endl;
    Serial << "  exitTime:     " << getExitTime() << endl;
    Serial << "  isDone:       " << isDone() << endl;
}


const char* Photogate::getStateStr()
{
    switch (getState())
    {
        case READY:
            return "READY";

        case MEASURING:
            return "MEASURING";

        case DONE:
            return "DONE";

        default:
            return "UNKNOWN";
    }
}


// Photogate Protected methods
// ----------------------------------------------------------------------------

void Photogate::setAllBitMaskAndPort()
{
    setSignalBitMaskAndPort();
    setLedBitMaskAndPort();
    setAutoDetectBitMaskAndPort();
}

void Photogate::setSignalBitMaskAndPort()
{
    signalPinBitMask_ = digitalPinToBitMask(config_.signalPin);
    uint8_t signalPort = digitalPinToPort(config_.signalPin);
    signalPortInReg_ = portInputRegister(signalPort);
}


void Photogate::setLedBitMaskAndPort()
{
    ledPinBitMask_ = digitalPinToBitMask(config_.ledPin);
    uint8_t ledPort = digitalPinToPort(config_.ledPin);
    ledPortOutReg_ = portOutputRegister(ledPort);
}


void Photogate::setAutoDetectBitMaskAndPort()
{
    autoDetectPinBitMask_ = digitalPinToBitMask(config_.autoDetectPin);
    uint8_t autoDetectPort = digitalPinToPort(config_.autoDetectPin);
    autoDetectPortInReg_ = portInputRegister(autoDetectPort);
}
