# pxt-binbot-wit-2020

A MakeCode extensions for WITs Binbot Project

Originally developed by [robertsausg](https://github.com/robertsausg/pxt-binbot-wit).

## Usage


### Setting the Radio Group

```blocks
radio.setGroup(187)
```

### Moving Binbot

```blocks
input.onButtonPressed(Button.A, function () {
    Binbot.moveBinbot(100, 0, 0)
})
```

## License
MIT

## Supported targets

* for PXT/microbit
(The metadata above is needed for package search.)
