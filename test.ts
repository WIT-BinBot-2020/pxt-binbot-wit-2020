// tests go here; this will not be compiled when this
// package is used as a library
input.onButtonPressed(Button.B, function () {
    start = 0
    Binbot.moveBinbot(0, 0, 0)
})
input.onButtonPressed(Button.A, function () {
    start = 1
})
let start = 0
let sensor = 0
radio.setGroup(187)
basic.forever(function () {

    if (start == 1) {
        Binbot.moveBinbot(input.acceleration(Dimension.X), input.acceleration(Dimension.Y), 0)
    } else {
        Binbot.moveBinbot(0, 0, 0)

    }
    basic.pause(100)

})
basic.forever(function () {
    for (let index = 0; index <= 8; index++) {
        sensor = Binbot.requestSensor(index)
        console.logValue("Sensor Value " + index.toString() + " : ", sensor)
        if (sensor > 1000) {
            start = 0
            Binbot.moveBinbot(0, 0, 0)
        }

    }
    basic.pause(100)
})