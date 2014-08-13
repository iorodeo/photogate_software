#ifndef SYSTEM_STATE_H
#define SYSTEM_STATE_H
#include "photogate.h"
#include "constants.h"

class SystemState
{
    public:
        enum OperatingMode {NO_PHOTOGATE=0, ONE_PHOTOGATE, TWO_PHOTOGATE};

        SystemState();
        void initialize();
        void update();
        void reset();
        bool isDone();
        void handleSerialRequest();
        void sendListData();
        void sendJsonData();
        void sendPrettyData();
        void onPhotogatePinChange(int photogateNum);
        unsigned long getRunTime();
        const char* getOperatingModeStr();

    protected:
        Photogate photogate_[constants::NUMBER_OF_PHOTOGATES];
        unsigned long startTime_;
        OperatingMode operatingMode_;
        bool running_;
        bool timeout_;

        void checkOperatingMode();
        void checkForResetButton();
        void checkRunTime();
        void checkForDone();
        void updatePhotogateLed();
        
};

#endif

