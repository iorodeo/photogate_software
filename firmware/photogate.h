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
        bool isConnected();
        void reset();

        PhotogateConfig getConfig();
        void setConfig(PhotogateConfig config);
        int getLedPin();
        void setLedPin(int pinNum);
        int getSignalPin();
        void setSignalPin(int pinNum);
        int getAutoDetectPin();
        void setAutoDetectPin(int pinNum); 
        int getInterruptNum();
        void printConfig();
        inline void setLedOn();
        inline void setLedOff();
        inline int getSignal();
        inline State getState();

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
        volatile uint8_t *autoDetectPortOutReg_;
        volatile uint8_t *signalPortInReg_;

        void updateLedBitMaskAndPort();
        void updateSignalBitMaskAndPort();
        void updateAutoDetectBitMaskAndPort();
        void updateAllBitMaskAndPort();

};


inline void Photogate::setLedOn()
{
    *ledPortOutReg_ &= ~ledPinBitMask_;
}


inline void Photogate::setLedOff()
{
    *ledPortOutReg_ |= ledPinBitMask_;
}


inline int Photogate::getSignal()
{
    if (*signalPortInReg_ & signalPinBitMask_)
    {
        return true;
    }
    else
    {
        return false;
    }
}


inline Photogate::State Photogate::getState()
{
    return state_;
}
 
#endif
