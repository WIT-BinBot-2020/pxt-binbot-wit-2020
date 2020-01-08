#include "robotino.h"

ComId connectRobotino(){
    
    ComId com = Com_construct();
     Com_setAddress( com, ADDRESS);
    if( FALSE == Com_connect(com))
    {
        perror("Error on connect");
        return -1;
    }
    else{
        printf("Connected to %s\n",ADDRESS);
        return com;
    }
    
}

OmniDriveId initOmniDrive(ComId com){
    
    OmniDriveId omniDrive = OmniDrive_construct();
    if( INVALID_OMNIDRIVEID == omniDrive)
    {
        return -1;
    }
    
    if(FALSE == OmniDrive_setComId(omniDrive, com))
    {
        return -1;
    }
    return omniDrive;
    
}


void initDistanceSensors(ComId com, int ids[9]){
    
    int i = 0;
    
    for (i = 0; i < 9; i++)
    {
       ids[i] = DistanceSensor_construct(i);
       DistanceSensor_setComId(ids[i],com);
    }   
    
}
