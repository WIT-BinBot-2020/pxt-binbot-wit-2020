enum Commands {
    CMD_TEST = 0,
    CMD_SENDSTRING = 1,
    CMD_SENDNUMBERS = 2,
    CMD_CTRLOMNIDRIVE = 3,
    CMD_REQUESTDISTANCESENSOR = 4,
    CMD_SENDDISTANCESENSORVALUE = 5,
    CMD_REQUESTSOUND = 6,
    CMD_SENDNAME = 7
}

enum DistanceSensors {
    //% block="0"
    FRONT = 0,
    //% block="1"
    FRONT_LEFT = 1,
    //% block="2"
    LEFT_FRONT = 2,
    //% block="3"
    LEFT_BACK = 3,
    //% block="4"
    BACK_LEFT = 4,
    //% block="5"
    BACK_RIGHT = 5,
    //% block="6"
    RIGHT_BACK = 6,
    //% block="7"
    RIGHT_FRONT = 7,
    //% block="8"
    FRONT_RIGHT = 8
}

enum Sounds {
    //% block="Sound 0"
    SOUND_ZERO = 0,
    //% block="Sound 1"
    SOUND_ONE = 1,
    //% block="Sound 2"
    SOUND_TWO = 2,
    //% block="Sound 3"
    SOUND_THREE = 3,
    //% block="Sound 4"
    SOUND_FOUR = 4,
    //% block="Sound 5"
    SOUND_FIVE = 5,
    //% block="Sound 6"
    SOUND_SIX = 6,
    //% block="Sound 7"
    SOUND_SEVEN = 7,
    //% block="Sound 8"
    SOUND_EIGHT = 8
}


/**
 * Custom blocks
 */
//% weight=100 color=#0fbc11 icon=""
namespace Binbot {

    /**
    * Move Binbot
    * @param x speed in x direction, eg: 100
    * @param y speed in y direction, eg: 100
    * @param z rotation speed
    */
    //% block
    export function moveBinbot(x: number, y: number, z: number): void {

        sendPacket(createNumberPacket(Commands.CMD_CTRLOMNIDRIVE, x, y, z))
        // Add code here
    }

    /**
    * Request Sensor data
    * @param sensor sensor to request, eg: FRONT
    */
    //% block
    export function requestSensor(sensor: DistanceSensors): number {

        let res: Buffer
        sendPacket(createNumberPacket(Commands.CMD_REQUESTDISTANCESENSOR, sensor, 0, 0))
        res = receivePacket()

        if (res != null) {
            if (res.getNumber(NumberFormat.Int32LE, 0) == sensor) {
                return res.getNumber(NumberFormat.Int32LE, 4)
            }
            else {
                console.log("Error wrong sensor data")
                return null
            }

        }
        else {
            console.log("Error requesting sensor data")
            return null
        }
    }

    /**
    * Request Sound
    * @param sound sound to request i.e sound 1
    */
    //% block
    export function requestSound(sound:Sounds): number {

      let res: Buffer
      sendPacket(createNumberPacket(Commands.CMD_REQUESTSOUND, sound, 0, 0))
      res = receivePacket()

      if (res != null) {
          if (res.getNumber(NumberFormat.Int32LE, 0) == sensor) {
              return res.getNumber(NumberFormat.Int32LE, 4)
          }
          else {
              console.log("Error wrong sound data")
              return null
          }

      }
      else {
          console.log("Error requesting sound")
          return null
      }

    }

    /**
    * Send name
    * @param name name to set for the bot i.e Alexa
    */
    //% block
    export function sendName(name: string): void {
      
      sendPacket(createStringPacket(Commands.CMD_SENDNAME, name))

    }

    export function sendNumbers(x: number, y: number, z: number): void {

        sendPacket(createNumberPacket(Commands.CMD_SENDNUMBERS, x, y, z))

    }


    export function sendString(str: string): void {

        sendPacket(createStringPacket(Commands.CMD_SENDSTRING, str))

    }

    export function receiveString(): string {

        let res: Buffer = receivePacket()

        if (res != null) {
            return res.toString()
        }
        else {
            console.log("Error receiving string")
            return null
        }

    }

    function sendPacket(packet: Buffer): void {

        radio.sendRawPacket(packet)
    }

    function createStringPacket(cmd: Commands, str: string): Buffer {

        let msg: Buffer = control.createBuffer(12)
        let str_buf: Buffer = control.createBufferFromUTF8(str)
        if (str_buf.length > 12) {
            str_buf = str_buf.slice(0, 12)
        }
        msg.write(0, str_buf)

        return createPacket(cmd, msg)
    }

    function createNumberPacket(cmd: Commands, num1: number, num2: number, num3: number): Buffer {

        let msg: Buffer = control.createBuffer(12)
        msg.setNumber(NumberFormat.Int32LE, 0, num1)
        msg.setNumber(NumberFormat.Int32LE, 4, num2)
        msg.setNumber(NumberFormat.Int32LE, 8, num3)

        return createPacket(cmd, msg)
    }

    function createPacket(cmd: Commands, msg: Buffer): Buffer {
        let packet: Buffer = control.createBuffer(16)
        if (msg.length != 12) {
            console.log("wrong msg size")

        }
        else {

            let checksum: number = 0
            packet.setUint8(0, 0xbb)
            packet.setUint8(1, 0x00)
            packet.setUint8(2, cmd)
            packet.write(3, msg)

            for (let index = 0; index < 15; index++) {
                checksum ^= packet[index]
            }
            packet.setUint8(15, checksum)
            console.log("Packet: " + packet.toHex())


        }
        return packet
    }

    function receivePacket(timeout = 100): Buffer {
        let buf: Buffer = radio.readRawPacket()
        let checksum: number = 0
        let time: number = 0

        while (buf.length == 0) {

            if (timeout != 0) {
                if (time < timeout) {
                    time = time + 10
                }
                else {
                    console.log("Timeout receiving Packet")
                    return null
                }
            }
            basic.pause(10)
            buf = radio.readRawPacket()
        }
        if (buf.length == 16) {
            if (buf.getUint8(0) == 0xbb) {
                console.log(buf.toHex())
                for (let index = 0; index < 16; index++) {
                    checksum ^= buf[index]
                }

                if (checksum == 0) {
                    return buf.slice(3, 12)
                }
                else {
                    console.log("Error Checksum : " + checksum.toString())
                    return null
                }
            }
            else {
                console.log("Error Packetformat")
                return null
            }
        }
        else {
            console.log("Error length:" + buf.length.toString())
            return null
        }

    }
}
