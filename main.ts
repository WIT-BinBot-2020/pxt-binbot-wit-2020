function send_msg(msg: Buffer): void {

    if (msg.length != 12) {
        console.log("wrong msg size")
    }
    else {
        let packet: Buffer = control.createBuffer(16)
        let checksum: number = 0
        packet.setUint8(0, 0xbb)
        packet.setUint8(1, 0x01)
        packet.setUint8(2, 0xAA)
        packet.write(3, msg)

        for (let index = 0; index < 15; index++) {
            checksum ^= packet[index]
        }

        packet.setUint8(15, checksum)
        console.log("Packet: " + packet.toHex())

        radio.sendBuffer(packet)

    }


}

/**
 * Custom blocks
 */
//% weight=100 color=#0fbc11 icon=""
namespace custom {
    /**
     * TODO: describe your function here
     * @param n describe parameter here, eg: 5
     * @param s describe parameter here, eg: "Hello"
     * @param e describe parameter here
     */
    //% block
    export function send_accelerometer(x: number, y: number, z: number): void {

        let msg: Buffer = control.createBuffer(12)
        msg.setNumber(NumberFormat.Int32BE, 0, x)
        msg.setNumber(NumberFormat.Int32BE, 4, y)
        msg.setNumber(NumberFormat.Int32BE, 8, z)

        send_msg(msg)
        // Add code here
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