# Kaput!
A simple program that corrupts files in a variety of different ways!

## Examples
* Corrupt 30 random bytes in the file: ```kaput <input> <output> 30```
* Corrupt the entire file: ```kaput <input> <output> 0```
* Corrupt 30 bytes in offset range 30-100: ```kaput <input> <output> 30 -r 30-100```
* Corrupt all bytes in offset ranges 30-100, 60-200 and 300 to the end of the file: ```kaput <input> <output> 0 -r 30-100,60-200,300-end```
* Invert 30 random bytes in the file: ```kaput <input> <output> 30 -i```
* Corrupt every second byte for 30 bytes: ```kaput <input> <output> 30 -s 1```
* Invert every third byte in offset ranges 50-100 and 150-200, for 10 bytes in each range: ```kaput <input> <output> 10 -i -s 2 -r 50-100,150-200```
* Invert every second byte in offset range 50-100: ```kaput <input> <output> 0 -i -s 1 -r 50-100```