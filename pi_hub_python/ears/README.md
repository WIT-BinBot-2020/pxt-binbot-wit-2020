# Project Title

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run on an RPi, the following commands should get you up to speed...

PocketSphinx requirements:

```
sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev
pip install pocketsphinx
```
SpeechRecognition requirements:
```

```

### Special / Unique Sounding Keywords

The PocketSphinx 'pronounciation-dictionary.dict' within the 'speech_recognition' module, contains a huge list of english words. However, if you are hoping to have your own unique word, such as "BinBot" recognised, you'll need to add it to the dictionary. The easiest way to do this is by finding existing words that partially represent your word's sounds - copying them to assemble your own.
For this project: "BinBot" must be added to 'pronounciation-dictionary.dict'
As there are a few ways to pronounce the word, multiple can be added as shown below with (#).
```
binbot B IH N B AH T
binbot(2) B IH N B AA T
binbot(3) B IH N B AH
```
Your dictionary location may be different - but try here first:
/home/pi/.local/lib/python3.5/site-packages/speech_recognition/pocketsphinx-data/en-US


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

