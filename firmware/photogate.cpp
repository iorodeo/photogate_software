#include "photogate.h"
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
    updateAllBitMaskAndPort();
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
    updateLedBitMaskAndPort();
}


int Photogate::getSignalPin()
{
    return config_.signalPin;
}

void Photogate::setSignalPin(int pinNum)
{
    config_.signalPin = pinNum;
    updateSignalBitMaskAndPort();
}


int Photogate::getAutoDetectPin()
{
    return config_.autoDetectPin;
}


void Photogate::setAutoDetectPin(int pinNum)
{
    config_.autoDetectPin = pinNum;
    updateAutoDetectBitMaskAndPort();
}


int Photogate::getInterruptNum()
{
    return config_.interruptNum;
}


unsigned long  Photogate::getEntryTime()
{
    return entryTime_;
}


unsigned long  Photogate::getExitTime()
{
    return exitTime_;
}


bool Photogate::hasEntryTime()
{
    if (state_ != READY)
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
    if (state_ == DONE)
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
    Serial << state_ << ',';
    Serial << hasEntryTime() << ',';
    Serial << entryTime_ << ',';
    Serial << hasExitTime() << ',';
    Serial << exitTime_ << ',';
    Serial << isDone() << ',';
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
    Serial << "  state:        " << state_ << endl;
    Serial << "  hasEntryTime: " << hasEntryTime() << endl;
    Serial << "  entryTime:    " << entryTime_ << endl;
    Serial << "  hasExitTime:  " << hasExitTime() << endl;
    Serial << "  exitTime:     " << exitTime_ << endl;
    Serial << "  isDone:       " << isDone() << endl;
}


const char* Photogate::getStateStr()
{
    switch (state_)
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

void Photogate::updateAllBitMaskAndPort()
{
    updateSignalBitMaskAndPort();
    updateLedBitMaskAndPort();
    updateAutoDetectBitMaskAndPort();
}

void Photogate::updateSignalBitMaskAndPort()
{
    signalPinBitMask_ = digitalPinToBitMask(config_.signalPin);
    uint8_t signalPort = digitalPinToPort(config_.signalPin);
    signalPortInReg_ = portInputRegister(signalPort);
}


void Photogate::updateLedBitMaskAndPort()
{
    ledPinBitMask_ = digitalPinToBitMask(config_.ledPin);
    uint8_t ledPort = digitalPinToPort(config_.ledPin);
    ledPortOutReg_ = portOutputRegister(ledPort);
}


void Photogate::updateAutoDetectBitMaskAndPort()
{
    autoDetectPinBitMask_ = digitalPinToBitMask(config_.autoDetectPin);
    uint8_t autoDetectPort = digitalPinToPort(config_.autoDetectPin);
    autoDetectPortInReg_ = portInputRegister(autoDetectPort);
}
