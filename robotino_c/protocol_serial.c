
#include "protocol_serial.h"


PROTO_ERR_t initSerialCOM(int *fd, Termios* mytio){
    
    
    *fd = open(MODEMDEVICE, O_RDWR | O_NOCTTY); 
    if (*fd <0) {perror(MODEMDEVICE); return ERROR_OPENING_COM; }
    
    bzero(mytio, sizeof(*mytio));
    mytio->c_cflag = BAUDRATE | CRTSCTS | CS8 | CLOCAL | CREAD;
    mytio->c_iflag = IGNPAR;
    mytio->c_oflag = 0;
    
    /* set input mode (non-canonical, no echo,...) */
    mytio->c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    mytio->c_cc[VTIME] = 0;
    mytio->c_cc[VMIN] = 16;
    
    tcflush(*fd, TCIFLUSH);
    tcsetattr(*fd,TCSANOW,mytio);
    
    return 0;
    
}



PROTO_ERR_t sendPacket(int fd, packet_t *packet)
{
    int res = 0;
    res = write(fd,packet->buf,16);
    
    if(res != 16)
    {
        return ERROR_SENDING;
    }
    
    return NO_ERROR;
}

PROTO_ERR_t createPacket(packet_t* packet, commands_t cmd, unsigned char *buf)
{
    unsigned char checksum = 0;
    int i = 0;
    
    bzero(packet->buf,16);
    packet->buf[0] = 0xbb;
    packet->buf[1] = 0x00;
    packet->buf[2] = (char)cmd;
    
    memcpy((packet->buf) + 3, buf, 12);
    
    for(i = 0; i <15; i++)
    {
        checksum ^= packet->buf[i];
    }
    packet->buf[15] = checksum;
    
    return NO_ERROR;
    
}

PROTO_ERR_t createStringPacket(packet_t* packet, commands_t cmd, unsigned char *str, int len)
{
    
    unsigned char buf[12] = {0};
    if(len > 12)
    {
        printf("Message too long - max 12 chars\n");
        len = 12;
    }
    memcpy(buf,str,len);
    
    return createPacket(packet,cmd,buf);
}

PROTO_ERR_t createNumberPacket(packet_t* packet, commands_t cmd, int num1, int num2, int num3)
{
    unsigned char buf[12] = {0};
    
    memcpy(buf,&num1,4);
    memcpy(buf+4,&num2,4);
    memcpy(buf+8,&num3,4);
    
    return createPacket(packet,cmd,buf);
}



PROTO_ERR_t receivePacket(int fd, packet_t* packet)
{
    unsigned char buf[255] = {0};
    int res = 0;
    int i = 0;
    unsigned char checksum = 0;
    bzero(packet->buf,16);

    do
    {
    res = read(fd,buf,255);
    }while(res != 16);

    
    for(i = 0; i < res; i++)
    {
        checksum ^= buf[i];
    }

    memcpy(packet->buf,buf,16);
    
    if(checksum != 0)
    {
    	return ERROR_RECEIVING;
        
	
    } 
	
    return NO_ERROR;
 
}

PROTO_ERR_t decodePacket(msg_t* msg_data, packet_t* packet)
{
    msg_data->cmd = (commands_t)packet->buf[2];
    
    strncpy(msg_data->str,(packet->buf)+3,12);
    msg_data->num1 = *(int *)((packet->buf)+3);
    msg_data->num2 = *(int *)((packet->buf)+7);
    msg_data->num3 = *(int *)((packet->buf)+11);
    
    return NO_ERROR;
}
