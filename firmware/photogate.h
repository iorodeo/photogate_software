#ifndef PHOTOGATE_H
#define PHOTOGATE_H 
#include "constants.h"
#include <Arduino.h>

struct PhotogateConfig
{
    int ledPin;
    int signalPin;
    int autoDetectPin;
    int interruptNum;
};
const PhotogateConfig DEFAULT_CONFIG = {6,2,4,0};


class Photogate
{
    public:

        enum State {READY, MEASURING, DONE};

        Photogate(PhotogateConfig config=DEFAULT_CONFIG);
        void initialize();
        bool isInitialized();
        void reset();

        PhotogateConfig getConfig();
        void setConfig(PhotogateConfig config);
        void printConfig();

        int getLedPin();
        void setLedPin(int pinNum);

        int getSignalPin();
        void setSignalPin(int pinNum);

        int getAutoDetectPin();
        void setAutoDetectPin(int pinNum); 

        int getInterruptNum();


        inline void setLedOn();
        inline void setLedOff();
        inline void setLedFromSignal();
        inline int getSignal();
        inline State getState();
        inline bool isConnected();

    protected:

        PhotogateConfig config_;
        unsigned long entryTime_;
        unsigned long exitTime_;
        State state_;
        bool initFlag_;

        // Store pin masks and port output registers for faster digital IO
        uint8_t ledPinBitMask_;
        uint8_t autoDetectPinBitMask_;
        uint8_t signalPinBitMask_;

        volatile uint8_t *ledPortOutReg_;
        volatile uint8_t *autoDetectPortInReg_;
        volatile uint8_t *signalPortInReg_;

        void updateLedBitMaskAndPort();
        void updateSignalBitMaskAndPort();
        void updateAutoDetectBitMaskAndPort();
        void updateAllBitMaskAndPort();

};


inline void Photogate::setLedOn()
{
    *ledPortOutReg_ |= ledPinBitMask_;
}


inline void Photogate::setLedOff()
{
    *ledPortOutReg_ &= ~ledPinBitMask_;
}


inline void Photogate::setLedFromSignal()
{
    int signal = getSignal();
    if (isConnected())
    {
        if (signal == LOW)
        {
            setLedOff();
        }
        else
        {
            setLedOn();
        }
    }
    else
    {
        setLedOff();
    }
}


inline int Photogate::getSignal()
{
    if (*signalPortInReg_ & signalPinBitMask_)
    {
        return HIGH;
    }
    else
    {
        return LOW; 
    }
}


inline Photogate::State Photogate::getState()
{
    return state_;
}
 

inline bool Photogate::isConnected()
{
    if (*autoDetectPortInReg_ & autoDetectPinBitMask_)
    {
        return false;
    }
    else
    {
        return true;
    }
}

#endif
