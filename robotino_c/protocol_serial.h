/*!
\file protocol_serial.h
\author Robert Sausgruber
\date 01.12.2019
\version 1.0

\brief Header File for the serial protocol of the Binbot Project
*/

#ifndef PROTO_SERIAL_H_
#define PROTO_SERIAL_H_

#include <stdio.h>
#include <fcntl.h>  /* File Control Definitions          */
#include <termios.h>/* POSIX Terminal Control Definitions*/
#include <unistd.h> /* UNIX Standard Definitions         */
//#include <errno.h>  /* ERROR Number Definitions          */
#include <stdlib.h>
#include <string.h>
//#include <sys/types.h>
//#include <sys/stat.h>


typedef struct termios Termios;

#define BAUDRATE B115200
#define MODEMDEVICE "/dev/ttyACM0"
//#define _POSIX_SOURCE 1 /* POSIX compliant source */

#define PROTO_LENGTH 16

typedef enum PROTO_ERR
{
  NO_ERROR = 0,
  UNKNOWN_ERROR = -1,
  ERROR_OPENING_COM = -2,
  ERROR_SENDING = -4,
  ERROR_RECEIVING = -8,
  
} PROTO_ERR_t;

typedef enum Commands {
    CMD_TEST  = 0,
    CMD_SENDSTRING = 1,
    CMD_SENDNUMBERS = 2,
    CMD_CTRLOMNIDRIVE = 3,
    CMD_REQUESTDISTANCESENSOR = 4,
    CMD_SENDDISTANCESENSORVALUE = 5,
    
}commands_t;

typedef struct packet {
   unsigned char buf[16];
    
} packet_t;

typedef struct msg_data {
    commands_t cmd;
    unsigned char str[12];
    int num1;
    int num2;
    int num3;
} msg_t;


PROTO_ERR_t initSerialCOM(int *fd, Termios* mytio);

PROTO_ERR_t sendPacket(int fd, packet_t* packet); //sendsPacket 

PROTO_ERR_t createStringPacket(packet_t* packet, commands_t cmd, unsigned char *str, int len); //Creates String Message and creates Packet
PROTO_ERR_t createNumberPacket(packet_t* packet, commands_t cmd, int num1,int num2,int num3); //Creates Number Message and creates Packet


PROTO_ERR_t createPacket(packet_t* packet, commands_t cmd,unsigned char *buf); //Adds Header and Checksum


PROTO_ERR_t receivePacket(int fd, packet_t* packet); //receives 16 Byte Packet and does checksum check

PROTO_ERR_t decodePacket(msg_t* msg_data, packet_t* packet); //gives numbers and string

#endif /* PROTO_SERIAL_H_ */

/* EOF */
