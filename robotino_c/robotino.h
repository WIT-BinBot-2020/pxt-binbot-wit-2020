/*!
\file robotino.h
\author Robert Sausgruber
\date 02.12.2019
\version 1.0

\brief Header File for the robotino control of the Binbot Project
*/

#ifndef ROBOTINO_H_
#define ROBOTINO_H_

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <fcntl.h> 
#include <sys/stat.h> 
#include <sys/types.h> 
#include <unistd.h>

#include "rec/robotino/com/c/Com.h"
#include "rec/robotino/com/c/OmniDrive.h"
#include "rec/robotino/com/c/DistanceSensor.h"


#define ADDRESS "127.0.0.1"

enum DistanceSensors {
    FRONT = 0,
    FRONT_LEFT = 1,
    FRONT_RIGHT = 8,
    LEFT_FRONT = 2,
    LEFT_BACK = 3,
    BACK_LEFT = 4,
    BACK_RIGHT =5,
    RIGHT_BACK = 6,
    RIGHT_FRONT = 7
};



ComId connectRobotino();

OmniDriveId initOmniDrive(ComId com);
void initDistanceSensors(ComId com, int ids[9]);



#endif /* ROBOTINO_H_ */

/* EOF */
