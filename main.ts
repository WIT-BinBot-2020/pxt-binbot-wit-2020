enum Commands {
    testMessage = 0,
    send12Chars = 1,
    send3Numbers = 2,
    controlBinbot = 3
}


function sendPacket(msg: Buffer, cmd: Commands): void {

    if (msg.length != 12) {
        console.log("wrong msg size")
    }
    else {
        let packet: Buffer = control.createBuffer(16)
        let checksum: number = 0
        packet.setUint8(0, 0xbb)
        packet.setUint8(1, 0x00)
        packet.setUint8(2, 0xAA)
        packet.write(3, msg)

        for (let index = 0; index < 15; index++) {
            checksum ^= packet[index]
        }

        packet.setUint8(15, checksum)
        console.log("Packet: " + packet.toHex())

        radio.sendRawPacket(packet)

    }
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

        let msg: Buffer = control.createBuffer(12)
        msg.setNumber(NumberFormat.Int32BE, 0, x)
        msg.setNumber(NumberFormat.Int32BE, 4, y)
        msg.setNumber(NumberFormat.Int32BE, 8, z)

        sendPacket(msg,Commands.send3Numbers)
        // Add code here
    }

    /**
 * TODO: describe your function here
 * @param n describe parameter here, eg: 5
 * @param s describe parameter here, eg: "Hello"
 * @param e describe parameter here
 */
    //% block
    export function sendString(str: string): void {


        let msg: Buffer = control.createBufferFromUTF8(str)
        if (msg.length > 12) {
            msg = msg.slice(0, 12)
        }

        sendPacket(msg,Commands.send12Chars)

    }

    /**
    * TODO: describe your function here
    * @param n describe parameter here, eg: 5
    * @param s describe parameter here, eg: "Hello"
    * @param e describe parameter here
    */
    //% block
    export function moveBinbot(x: number, y: number, z: number): void {

        let msg: Buffer = control.createBuffer(12)
        msg.setNumber(NumberFormat.Int32BE, 0, x)
        msg.setNumber(NumberFormat.Int32BE, 4, y)
        msg.setNumber(NumberFormat.Int32BE, 8, z)

        sendPacket(msg, Commands.controlBinbot)
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
                    return buf.slice(3, 12).toString()
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

    /**
     * TODO: describe your function here
     * @param value describe value here, eg: 5
     */
    //% block
    export function fib(value: number): number {
        return value <= 1 ? value : fib(value - 1) + fib(value - 2);
    }
}