# Raspberry PI Hub

This is the directory where you can input all your Python files that will be stored in the Raspberry Pi Hub!

## Communications

### Communication with Main Hub File

Make sure that your Python code's different functionalities is modularised in functions. This will allow the Main Hub File to call them.

### Example

`helloWorld.py`
```python
def printHelloWorld():
  print("Hello World")
```

`pi_hub.py`
```python
import helloWorld

...
...

while True:
    
    ...
    ...

    helloWorld.printHelloWorld()
```