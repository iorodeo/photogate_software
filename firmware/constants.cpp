#include "constants.h"
#include "photogate.h"


namespace constants
{
    const long BAUDRATE = 115200;
    const int RESET_PIN = 8;
    const unsigned long MAXIMUM_RUNTIME = 3600000000; // 60 min
    const PhotogateConfig PHOTOGATE_CONFIG[NUMBER_OF_PHOTOGATES] = 
    {
        {6,2,4,0},  // Photogate 0, {LED, Signal, AutoDetect, interruptNum}
        {7,3,5,1}   // Photogate 1,   "     "         "            "
    };
}
