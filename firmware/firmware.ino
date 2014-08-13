#include <Streaming.h>
#include "firmware.h"
#include "constants.h"
#include "utility.h"
#include "photogate.h"
#include "system_state.h"

SystemState systemState;

void setup()
{
    systemState.initialize();
}

void loop()
{
    systemState.update();
    systemState.handleSerialRequest();
}

void onPhotogatePinChange0()
{
    static int photogateNum = 0;
    systemState.onPhotogatePinChange(photogateNum);
}

void onPhotogatePinChange1()
{
    static int photogateNum = 1;
    systemState.onPhotogatePinChange(photogateNum);
}
