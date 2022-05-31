# PictureSort
Small program with a simple GUI to change meta data of pictures

## Idea
Smartphone pictures send with messenger apps usually influence meta data. This makes it duiffcult to sort them in the right order. 
*PictureSort* will help to change meta data and sort it naturally on the file system. 

The advantage: The pictures can be viewed ordered and the order is independet of software organizing pictures.

## Usage
![PictureSort Screenshot](/img/ps.png "PictureSort Screenshot")
Sorting pictures with PictureSort happens in three steps:
1. Selecting the picture folder
2. Ordering the pictures with a simple mouse click:
     - right click adds the picture to the current order
     - left click removes the last picture from the current order
3. Commiting the order and writing the changes to the files with one last button click

## Requirements
- Python 3.9.2
- [PyQt5](https://pypi.org/project/PyQt5/5.6/ "PyQt5")

## Binary Build Procedure
Currently binaries are available for *Linux* and *Windows*.
They are created separately on each plattform with [pyinstaller](https://pypi.org/project/pyinstaller/ "pyinstaller").

## Licence
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

**Icons**
Icons from [ionicons](https://github.com/ionic-team/ionicons "ionicons")
