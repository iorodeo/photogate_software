#ifndef CONSTANTS_H
#define CONSTANTS_H

struct PhotogateConfig;

namespace constants 
{

    enum {NUMBER_OF_PHOTOGATES=2};
    extern const PhotogateConfig PHOTOGATE_CONFIG[NUMBER_OF_PHOTOGATES];
    extern const int RESET_PIN;

}


#endif


