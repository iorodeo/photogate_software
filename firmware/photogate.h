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

        enum State {READY=0, MEASURING, DONE};

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

        unsigned long  getEntryTime(unsigned long startTime=0);
        unsigned long  getExitTime(unsigned long startTime=0);
        State getState();
        bool hasEntryTime();
        bool hasExitTime();
        bool isDone();

        void sendListData(unsigned long startTime=0);
        void sendJsonData(unsigned long startTime=0);
        void sendPrettyData(unsigned long startTime=0);
        const char* getStateStr();


        inline void setLedOn();
        inline void setLedOff();
        inline void setLedFromSignal();
        inline void setLedFromSignal(int signal);
        inline int getSignal();
        inline State getStateUnsafe();
        inline bool isConnected();
        inline void update();

    protected:

        bool initFlag_;
        PhotogateConfig config_;
        volatile unsigned long entryTime_;  // Value changed in interrupt 
        volatile unsigned long exitTime_;   // Value changed in interrupt
        volatile State state_;              // Value changed in interrupt

        // Store pin masks and port output registers for faster digital IO
        uint8_t ledPinBitMask_;
        uint8_t autoDetectPinBitMask_;
        uint8_t signalPinBitMask_;

        volatile uint8_t *ledPortOutReg_;
        volatile uint8_t *autoDetectPortInReg_;
        volatile uint8_t *signalPortInReg_;

        void setLedBitMaskAndPort();
        void setSignalBitMaskAndPort();
        void setAutoDetectBitMaskAndPort();
        void setAllBitMaskAndPort();

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
    setLedFromSignal(signal);
}


inline void Photogate::setLedFromSignal(int signal)
{
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


inline Photogate::State Photogate::getStateUnsafe()
{
    // Fast access function - only for use in interrupt or ATOMIC_BLOCK
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


inline void Photogate::update()
{
    int signal = getSignal();
    unsigned long eventTime = micros();

    if (isConnected())
    {
        switch (state_)
        {
            case READY:
                if (signal == LOW)
                {
                    entryTime_ = eventTime;
                    state_ = MEASURING;
                }
                break;

            case MEASURING:
                if (signal == HIGH)
                {
                    exitTime_ = eventTime;
                    state_ = DONE;
                }
                break;

            case DONE:
                break;

            default:
                break;
        }
    }
    setLedFromSignal(signal);
}

#endif
