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

        Photogate(PhotogateConfig config=DEFAULT_CONFIG);
        void initialize();

        bool isInitialized();
        bool isConnected();

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


    protected:

        PhotogateConfig config_;
        bool initFlag_;

        // Store pin masks and port output registers for faster digital IO
        uint8_t signalPinBitMask_;
        volatile uint8_t *signalPortOutReg_;
        uint8_t ledPinBitMask_;
        volatile uint8_t *ledPortOutReg_;
        uint8_t autoDetectPinBitMask_;
        volatile uint8_t *autoDetectPortOutReg_;

        void updateAllBitMaskAndPort();
        void updateSignalBitMaskAndPort();
        void updateLedBitMaskAndPort();
        void updateAutoDetectBitMaskAndPort();

};
 
#endif
