from pymouse import PyMouse
import time

mouse = PyMouse()
while True:
    print mouse.position()
    time.sleep(1)
