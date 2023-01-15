# PictureSort
Small program with a simple GUI to change meta data of pictures

## Idea
Smartphone pictures send with messenger apps usually influence meta data. This makes it difficult to sort them in the right order. 
*PictureSort* will help to change meta data and sort it naturally on the file system. 

The advantage: The pictures can be viewed ordered and the order is independet of software organizing pictures.

## Influenced meta data
The modified date is used as a sort criterium.
The time stamp of the first selected picture is used as reference and every preceeding picture gets added one more second to the reference time stamp.  

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
Currently binaries are available for *Linux* and *Windows 10*.
They are created separately on each plattform with [pyinstaller](https://pypi.org/project/pyinstaller/ "pyinstaller").
<table>
     <tr>
          <th columnspan="3">File</th>
          <th>Sum sha256</th>
          <th>Plattform</th>
     </tr>
     <tr>
          <td>PictureSort-1.0-win.zip</td>
          <td>816cd15104039bcd03b1ea17db98f3edad0ac9e94e1aef370dc1da00e1681b9c</td>
          <td>Windows 10</td>
     </tr>
     <tr>
          <td>PictureSort-1.0-linux.tar.gz</td>
          <td>978469a2ff00c1294500eac6fb5511bc0eb23e072e037608865177b53e43c21b</td>
          <td>Linux</td>
     </tr>
     <tr>
          <td>PictureSort-1.1-win.zip</td>
          <td>cedaf5d8689bec3d4ad3902139ea244c156dcffdc5f456b8cf6ebc27ab3e34b4</td>
          <td>Windows 10</td>
     </tr>
     <tr>
          <td>PictureSort-1.1-win11.zip</td>
          <td>b3fedec5d67554d3f7df24b43866a2dc6dd7a38be02cf42197c1aee14ddb2a4a</td>
          <td>Windows 11</td>
     </tr>
     <tr>
          <td>PictureSort-1.1-linux.tar.gz</td>
          <td>6f9ec9ad0b93103c3f2107a312d27c61ba14836907f18c8d5301b31d6c361599</td>
          <td>Linux</td>
     </tr>
</table>


## Licence
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

#### Icons
Icons from [ionicons](https://github.com/ionic-team/ionicons "ionicons")
