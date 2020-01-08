#include "protocol_serial.h"
#include "robotino.h"


int main()
{
    Termios newtio;
    int fd = 0;
    float v = 0.0;
    
    PROTO_ERR_t res = 0;
    
    
    
    ComId com = connectRobotino();
    if(com < 0) {return -1;}
    OmniDriveId omniDrive = initOmniDrive(com);
    if(omniDrive < 0) {return -1;}
    DistanceSensorId sensors[9];
    initDistanceSensors(com, sensors);
    
    res = initSerialCOM(&fd,&newtio);
    if(res <0 ) {return -1;}
    
    
    
    
    packet_t send_packet;
    packet_t rcv_packet;
    msg_t rcv_msg;
    
    while(Com_isConnected(com))
    {
       res = receivePacket(fd,&rcv_packet);
       if(res <0 ) {printf("Error packets\n"); return -1;}
       
       res += decodePacket(&rcv_msg,&rcv_packet);
        switch(rcv_msg.cmd){
            case CMD_SENDSTRING : 
            {
                printf("Received String: %.12s\n", rcv_msg.str); 
                break;
            }
            case CMD_SENDNUMBERS : 
            {
                printf("Received 3 numbers: %d, %d, %d\n",rcv_msg.num1,rcv_msg.num2,rcv_msg.num3); 
                break;
            }
            case CMD_CTRLOMNIDRIVE : 
            {
                if(!OmniDrive_setVelocity( omniDrive,rcv_msg.num1, rcv_msg.num2, rcv_msg.num3 )){
			printf("Error OmniDriveId");
		}
                printf("controlBinbot with %d %d %d\n",rcv_msg.num1, rcv_msg.num2, rcv_msg.num3); 
                break;
            }
          
            case CMD_REQUESTDISTANCESENSOR : 
            {
		v =  DistanceSensor_voltage(sensors[rcv_msg.num1]);
                res += createNumberPacket(&send_packet,CMD_SENDDISTANCESENSORVALUE,rcv_msg.num1,(int)(v*1000),0);
                res += sendPacket(fd,&send_packet);
                printf("Sensor %d's value sent: %f\n",rcv_msg.num1,v);
                break;
            }
            default : printf("Wrong CMD\n"); break;
        }
       
       if(res != 0)
       {
           printf("Error %d\n",res);
           exit(1);
       }
       
       
    }
printf("Connection Lost\n");    
    
}
