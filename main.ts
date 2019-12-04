enum Commands {
    CMD_TEST = 0,
    CMD_SENDSTRING = 1,
    CMD_SENDNUMBERS = 2,
    CMD_CTRLOMNIDRIVE = 3,
    CMD_REQUESTDISTANCESENSOR = 4,
    CMD_SENDDISTANCESENSORVALUE = 5,

}

enum DistanceSensors {
    FRONT = 0,
    FRONT_LEFT = 1,
    FRONT_RIGHT = 8,
    LEFT_FRONT = 2,
    LEFT_BACK = 3,
    BACK_LEFT = 4,
    BACK_RIGHT = 5,
    RIGHT_BACK = 6,
    RIGHT_FRONT = 7
};

let receive_str: string
let receive_num1: number
let receive_num2: number
let receive_num3: number

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


/**
 * Custom blocks
 */
//% weight=100 color=#0fbc11 icon=""
namespace Binbot {
    /**
     * TODO: describe your function here
     * @param n describe parameter here, eg: 5
     * @param s describe parameter here, eg: "Hello"
     * @param e describe parameter here
     */
    //% block
    export function sendNumbers(x: number, y: number, z: number): void {

        sendPacket(createNumberPacket(Commands.CMD_SENDNUMBERS, x, y, z))

    }

    /**
 * TODO: describe your function here
 * @param n describe parameter here, eg: 5
 * @param s describe parameter here, eg: "Hello"
 * @param e describe parameter here
 */
    //% block
    export function sendString(str: string): void {

        sendPacket(createStringPacket(Commands.CMD_SENDSTRING, str))

    }

    /**
    * TODO: describe your function here
    * @param n describe parameter here, eg: 5
    * @param s describe parameter here, eg: "Hello"
    * @param e describe parameter here
    */
    //% block
    export function moveBinbot(x: number, y: number, z: number): void {

        sendPacket(createNumberPacket(Commands.CMD_CTRLOMNIDRIVE, x, y, z))
        // Add code here
    }

    /**
* TODO: describe your function here
* @param n describe parameter here, eg: 5
* @param s describe parameter here, eg: "Hello"
* @param e describe parameter here
*/
    //% block
    export function requestSensor(sensor: DistanceSensors): void {

        sendPacket(createNumberPacket(Commands.CMD_REQUESTDISTANCESENSOR, sensor, 0, 0))
        // Add code here
    }


    /**
* TODO: describe your function here
* @param n describe parameter here, eg: 5
* @param s describe parameter here, eg: "Hello"
* @param e describe parameter here
*/
    //% block
    export function receiveString(): string {

        let buf: Buffer = radio.readRawPacket()
        let checksum: number = 0

        if (buf.length == 16) {
            if (buf.getUint8(0) == 0xbb) {
                console.log(buf.slice(3, 12).toHex())
                for (let index = 0; index < 16; index++) {
                    checksum ^= buf[index]
                }

                if (checksum == 0) {
                    receive_str = buf.slice(3, 12).toString()
                    receive_num1 = buf.getNumber(NumberFormat.Int32LE, 3)
                    receive_num2 = buf.getNumber(NumberFormat.Int32LE, 7)
                    receive_num3 = buf.getNumber(NumberFormat.Int32LE, 11)

                    console.log(receive_str)
                    console.log(receive_num1.toString())
                    console.log(receive_num2.toString())
                    console.log(receive_num3.toString())
                    return "Packet received"
                }
                else {
                    return "Error Checksum"
                }
            }
            else {
                return "Error Packetformat"
            }
        }
        else {
            return "Error length"
        }


    }

}