# Autocropper

In 2023 my first foray into embedded electronics was an RP2040 board with a built-in GC9A01 TFT display. I based my code largely on [these Circuitpython examples](https://github.com/todbot/CircuitPython_GC9A01_demos). I've since added an SD card reader, but needed a faster means of processing files to a format suitable for such small, embedded displays. This is my first pass.

This script will find faces present in an image, crop to a specified ratio, scale the image, and save as a `.bmp` file. I've added padding so that more of the context is captured, rather than the limits of the face bounding box(es).
