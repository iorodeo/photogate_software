#ifndef SYSTEM_STATE_H
#define SYSTEM_STATE_H
#include "photogate.h"
#include "constants.h"

class SystemState
{
    public:
        enum OperatingMode {NO_PHOTOGATE, ONE_PHOTOGATE, TWO_PHOTOGATE};
        
        SystemState();
        void initialize();
        void update();
        void reset();
        void onPhotogatePinChange(int photogateNum);

    protected:
        Photogate photogate_[constants::NUMBER_OF_PHOTOGATES];
        unsigned long startTime_;
        OperatingMode operatingMode_;

        void checkOperatingMode();
        void checkForResetButton();
        void updatePhotogateLed();
};

#endif

