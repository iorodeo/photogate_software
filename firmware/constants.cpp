#include "constants.h"
#include "photogate.h"


namespace constants
{
    const PhotogateConfig PHOTOGATE_CONFIG[NUM_PHOTOGATE] = 
    {
        {6,2,4,0},  // Photogate 0, {LED, Signal, AutoDetect, interruptNum}
        {7,3,5,1}   // Photogate 1,   "     "         "            "
    };
}
