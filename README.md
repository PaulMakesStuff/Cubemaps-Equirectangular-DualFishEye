# Generating Equirectangular Images

In time, this will become a collection of scripts to convert to and from equirectangular images and cube maps.

### Equirectangular from individual cube map files

Prior to using this script you will need to install [Python Imaging Library - PIL](http://www.pythonware.com/products/pil/). Once installed, copy the createEquiFromSquareFiles.py file to your computer. Open up either terminal, or command prompt and then run the following command replacing the file path with a path to the folder containing the six cube map images on your computer:

    python createEquiFromSquareFiles.py "/Users/paulreed/Dropbox/Virtual Reality/GitHub/"
    
Once complete the script will save an equirectangular image in the folder containing the six cube map images.

#### Licences
Cube map images the work of Emil Persson, aka Humus [http://www.humus.name] under a Creative Commons Attribution 3.0 Unported License. [http://creativecommons.org/licenses/by/3.0/]
