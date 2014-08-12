#include "constants.h"
#include "photogate.h"


namespace constants
{
    const PhotogateConfig PHOTOGATE_CONFIG[NUMBER_OF_PHOTOGATES] = 
    {
        {6,2,4,0},  // Photogate 0, {LED, Signal, AutoDetect, interruptNum}
        {7,3,5,1}   // Photogate 1,   "     "         "            "
    };

    const int RESET_PIN = 8;
}
