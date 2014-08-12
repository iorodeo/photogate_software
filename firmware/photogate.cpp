#include "photogate.h"
#include <Streaming.h>

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
};


bool Photogate::isInitialized()
{
    return initFlag_;
}


bool Photogate::isConnected()
{
    int pinValue = digitalRead(config_.autoDetectPin);
    if (pinValue == HIGH)
    {
        return false;
    }
    else
    {
        return true;
    }
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


void Photogate::printConfig()
{
    Serial << "ledPin         = " << config_.ledPin << endl;
    Serial << "signalPin      = " << config_.signalPin << endl;
    Serial << "autoDetectPin  = " << config_.autoDetectPin << endl;
    Serial << "interruptNum   = " << config_.interruptNum << endl;

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
    signalPortOutReg_ = portOutputRegister(signalPort);
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
    autoDetectPortOutReg_ = portOutputRegister(autoDetectPort);
}
