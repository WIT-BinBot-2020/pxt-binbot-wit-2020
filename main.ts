enum Commands {
    CMD_TEST = 0,
    CMD_SENDSTRING = 1,
    CMD_SENDNUMBERS = 2,
    CMD_CTRLOMNIDRIVE = 3,
    CMD_REQUESTDISTANCESENSOR = 4,
    CMD_SENDDISTANCESENSORVALUE = 5,
    CMD_REQUESTSOUND = 6,
    CMD_SENDNAME = 7,
    CMD_SENDMICTHRESHOLD = 8,
    CMD_BINMOUTH = 9,
    CMD_REQUESTMICANGLE = 10,
    CMD_REQUESTOBJCOORDS = 11,
    CMD_REQUESTNAMECALLED = 12
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

enum MouthState{
    //% block="Open"
    OPEN = 0,
    //% block="Closed"
    CLOSED = 1,
    //% block="Talk"
    TALK = 2,
    //% block="Munch"
    MUNCH = 3
}

enum Sounds {
    //% block="Mouth Open 0"
    SOUND_ZERO = 0,
    //% block="Mouth Close 1"
    SOUND_ONE = 1,
    //% block="Robot Stop 2"
    SOUND_TWO = 2,
    //% block="Shut down 3"
    SOUND_THREE = 3,
    //% block="Start Up 4"
    SOUND_FOUR = 4,
    //% block="Sound 5"
    //SOUND_FIVE = 5,
    //% block="Sound 6"
    //SOUND_SIX = 6,
    //% block="Sound 7"
    //SOUND_SEVEN = 7,
    //% block="Sound 8"
    //SOUND_EIGHT = 8
}

let voiceDetected: number = 0

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
    * Play Sound
    * @param sound sound to play i.e sound 1
    */
    //% block
    export function playSound(sound:Sounds): void {

      sendPacket(createNumberPacket(Commands.CMD_REQUESTSOUND, sound, 0, 0))

    }

    /**
    * Send name
    * @param name name to set for the bot i.e Alexa
    */
    //% block
    export function sendName(name: string): void {

      sendPacket(createStringPacket(Commands.CMD_SENDNAME, name))

    }

    /**
    * Send mic threshold
    * @param name set volume threshold for bot
    */
    //% block
    export function sendMicThreshold(threshold: number): void {

      let min: number = 0;
      let max: number = 255;
      if (threshold > max) {
        threshold = max;
      }
      else if (threshold < min){
        threshold = min
      }

      sendPacket(createNumberPacket(Commands.CMD_SENDMICTHRESHOLD, threshold, 0, 0))

    }

    /**
    * Toggle bin mouth state
    * @param mouthState
    */
    //% block
    export function sendMouthX(mouthState: MouthState): void {

      sendPacket(createNumberPacket(Commands.CMD_BINMOUTH, mouthState, 0, 0))

    }

    /**
    * Request Mic Angle
    * @param sensor requests angle at which sound was detected
    */
    //% block
    export function requestMicAngle(): number {

        let res: Buffer;
        let x: number = 0;

        sendPacket(createNumberPacket(Commands.CMD_REQUESTMICANGLE, 0, 0, 0))
        res = receivePacket()
        if (res != null) {
            x = res.getNumber(NumberFormat.Int32LE, 0)
            //A - B = 0 - 360
            //C - D = 0- 255
            let y = (x / 255) * 360
            return Math.abs(y)
        }
        else {
            console.log("Error requesting sensor data")
            return null
        }
    }

    /**
    * Request Object Coords
    */
    //% block
    export function requestObjectCoords(): {x: number, y:number} {

        let res: Buffer;
        let x: number;
        let y: number;
        sendPacket(createNumberPacket(Commands.CMD_REQUESTOBJCOORDS, 0, 0, 0))
        res = receivePacket()
        if (res != null) {
            x = res.getNumber(NumberFormat.Int32LE, 0)
            y = res.getNumber(NumberFormat.Int32LE, 4)
            return {x:x, y:y}
        }
        else {
            console.log("Error requesting sensor data")
            return null
        }
    }

    /**
    * Request Voice Detected
    * @param sensor requests whether or not the voice command was detected
    */
    //% block
    export function requestVoiceDetected(): number {

        let res: Buffer;
        let x: number;

        sendPacket(createNumberPacket(Commands.CMD_REQUESTNAMECALLED, 0, 0, 0))
        res = receivePacket()
        if (res != null) {
            x = res.getNumber(NumberFormat.Int32LE, 0)
            return x
        }
        else {
            console.log("Error requesting sensor data")
            return null
        }
    }

    /**
    * Request Voice Detected but we reset it to 0 in da code
    */
    //% block
    export function requestVoiceDetected2ElectricBoogaloo(): void {

        let res: Buffer;
        let x: number;

        sendPacket(createNumberPacket(Commands.CMD_REQUESTNAMECALLED, 0, 0, 0))
        res = receivePacket()
        if (res != null) {
            x = res.getNumber(NumberFormat.Int32LE, 0)
            if (x == 1) {
              voiceDetected = 1;
            }
        }
        else {
            console.log("Error requesting sensor data")
        }
    }

    /**
    * Set voiceDetected back to 0
    */
    //% block
    export function setVoiceDetected(): void {

      voiceDetected = 0;

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
