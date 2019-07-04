# P3M Python Metadata Media Manager

##### I have dumped all my photos in one folder for years and want to sort them by date!?! 
##### This is what you were searching for!

P3M is a script that allows you to sort and rename huge ammounts of files like images or videos by date. It is able to sort images (jpg/jpeg) depeding on their exif information and videos (mp4, mov) depending on their metadata. If a file has no metadata information it is also able to sort it by it's creation date.

To ensure nothing will happen to your precious memories P3M supports not only moving your images but also copying them or even backuping your files.

## Installation:
First of all install Python3!

The script uses two libraries [pyexif](http://pyexif.sourceforge.net/) and [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/) if you are on Arch Linux install them from AUR (python-piexif, python-pymediainfo). On any other platform just install them via pip:

```pip install pymediainfo```

```pip install pyexif```

Now you just need to download the script and you are good to go:

```git clone https://github.com/xeetsh/P3M```

## Usage:

##### ```python3 p3m.py -src <UNSORTED IMAGES> -dst <PATH TO SORT IMAGES TO> [options]```

    -h      --help                      Shows this help message and exits.
    -src    --source                    Source folder with images to sort. Usage: -src [SOURCE]
    -dst    --destination               Destination folder for the sorted images. Usage: -dst [DESTINATION]
    -r      --recursive                 Also scan subfolders for images to sort.
    -m      --move                      Moves the images instead of copying them (Think abouth backing up your images before with -b [DESTINATION]).
    -b      --backup                    Backs your images up your images before moving them. Usage: -b [DESTINATION].
    -n      --naming                    Set the naming of the images. Usage: -n [NAMING SCHEME]. Use -n -h for furhter information.
    -s      --sorting                   Set a folder sorting scheme. Usage: -s [SORTING SCHEME]. Use -s -h for further information.
    -a      --handleNodate              Moves or copies pictures that could not be sorted to a seperate folder named /NoDate/
    -c      --useCreationDate           Uses the creation date and time of a file as fallback if metainfo won't provide any information
    -v      --verbose                   Tells you everything that happens
    -xC                                 Don't ask for confirmation befor starting.
    -xB                                 Overrite old backup if there is one.
    -xO                                 Overrite files with duplicate names.
    
## Examples:

**Copy** all files from ImageDump/ to NicelySortedImages/ **rename** them that they have the **creation date and time as filename** and **sort** them into **folders by year and month**. If a file **has no creation date** in it's metadata use the **creation time of the file**.

```python3 p3m.py -src ImageDump/ -dst NicelySortedImages/ -n "YEAR-MONTH-DAY_HOUR-MINUTE-SECOND" -s "YEAR/MONTH" --useCreationDate```

**Move** all files from ImageDump/ **including subfolders** to NicelySortedImages/ and **sort** them in **folders based on their creation year**. If a file has **no creation date** **move** it to a **special folder**. **Backup all files** to a specific folder before moving them.

```python3 p3m.py -src ImageDump/ -r -dst NicelySortedImages/ -s "YEAR" --handleNodate --backup /Backup```

## Problems:

The script was never tested on Windows or Mac. Allthough it should run fine on these plattforms there is no guarantee. The "useCreationDate" feature may be a problem on non Linux platforms. Please report if you have tested this on a Windows or Mac machine.

Allthough this script is carefully tested and used by me quiet a lot, I can not assure you that this won't mess with your images. Eighter caused by wrong usage of the script or a bug. As you may intend to use this script to sort your precious images of that one special holliday in hawaii please be sure backup your images manually before you move them. You can allways delete them afterwards.
