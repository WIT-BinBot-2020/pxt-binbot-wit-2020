// tests go here; this will not be compiled when this package is used as a library
input.onButtonPressed(Button.B, function () {
    start = 0
    Binbot.moveBinbot(0, 0, 0)
})
input.onButtonPressed(Button.A, function () {
    start = 1
})
let start = 0
let front = 0
radio.setGroup(187)
basic.forever(function () {
    if (start == 1) {
        Binbot.moveBinbot(input.acceleration(Dimension.X), input.acceleration(Dimension.Y), 0)
        front = Binbot.requestSensor(DistanceSensors.FRONT)
        console.logValue("Front Sensor", front)
        basic.pause(100)
    }
})
