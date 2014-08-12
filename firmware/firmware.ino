#include <Streaming.h>
#include "firmware.h"
#include "system_state.h"
#include "photogate.h"
#include "constants.h"

SystemState systemState;

void setup()
{
    Serial.begin(115200);
    systemState.initialize();
}

void loop()
{
    systemState.update();
    delay(50);
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
