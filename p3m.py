# dependencys    python-piexif(ARCH-Linux AUR)
#               python-pymediainfo(ARCH-Linux AUR)

import sys
import piexif
import shutil
from pymediainfo import MediaInfo
from datetime import datetime
import os
import platform

print(piexif.__file__)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Image:
    __year = None
    __month = None
    __day = None
    __hour = None
    __minute = None
    __second = None
    __path = None
    __filetype = None

    def __init__(self, year, month, day, hour, minute, second, path, filetype):
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__path = path
        self.__filetype = filetype

    def toString(self):
        return self.__path + " " + self.__year + "-" + self.__month + "-" + self.__day + " " + self.__hour + ":" + self.__minute + ":" + self.__second + " " + self.__filetype


    # only creates an Image if there is exif information
    # returnes false if no image is created
    @staticmethod
    def create_image(path):
        try:
            filetype = os.path.splitext(path)[1]

            if filetype == ".mp4" or filetype == ".MP4" or filetype == ".MOV" or filetype == ".mov":
                media_info = MediaInfo.parse(path)
                for track in media_info.tracks:
                    if track.bit_rate is not None and track.track_type == "Video":
                        # get the videos recording date
                        date_time = track.tagged_date
                        year = date_time[4:8]
                        month = date_time[9:11]
                        day = date_time[12:14]
                        hour = date_time[15:17]
                        minute = date_time[18:20]
                        second = date_time[21:23]

                        # if there is no metadata in the video file the tagged_date is UTC 1904-01-01 00:00:00
                        if year == "1904" and use_creation_date == False:
                            print(bcolors.WARNING + "[ WARNING ] " + "Could not retrieve metadata information for: " + bcolors.ENDC + os.path.split(path)[1])

                            if handle_nodate:
                                move_or_copy_nodate(path)
                            
                            return False
                        
                        # FALLBACK
                        elif year == "1904" and use_creation_date:
                            date_time = get_time_from_creation_date(path)
                            year = date_time[0:4]
                            month = date_time[5:7]
                            day = date_time[8:10]
                            hour = date_time[11:13]
                            minute = date_time[14:16]
                            second = date_time[17:19]


            elif filetype == ".jpg" or filetype == ".JPG" or filetype == ".jpeg" or filetype == ".JPEG":
                # get exif information
                exif_dict = piexif.load(path)
                # exif36867 is the creation timestamp
                date_time = bytes.decode(exif_dict["Exif"][36867], "utf-8")
                year = date_time[0:4]
                month = date_time[5:7]
                day = date_time[8:10]
                hour = date_time[11:13]
                minute = date_time[14:16]
                second = date_time[17:19]

            # FALLBACK
            elif use_creation_date:
                date_time = get_time_from_creation_date(path)
                year = date_time[0:4]
                month = date_time[5:7]
                day = date_time[8:10]
                hour = date_time[11:13]
                minute = date_time[14:16]
                second = date_time[17:19]

            else:
                return False


            image = Image(year, month, day, hour, minute, second, path, filetype)

            return image

        except (KeyError, ValueError):
            print(bcolors.WARNING + "[ WARNING ] " + "Could not retrieve exif information for: " + bcolors.ENDC + os.path.split(path)[1])
            
            # FALLBACK
            if use_creation_date:
                date_time = get_time_from_creation_date(path)
                year = date_time[0:4]
                month = date_time[5:7]
                day = date_time[8:10]
                hour = date_time[11:13]
                minute = date_time[14:16]
                second = date_time[17:19]

                image = Image(year, month, day, hour, minute, second, path, filetype)

                return image

            if handle_nodate:
                move_or_copy_nodate(path)

            return False

        except TypeError:
            print(bcolors.WARNING + "[ WARNING ] " + "Could not retrieve metadata information for: " + bcolors.ENDC + os.path.split(path)[1])

            # FALLBACK
            if use_creation_date:
                date_time = get_time_from_creation_date(path)
                year = date_time[0:4]
                month = date_time[5:7]
                day = date_time[8:10]
                hour = date_time[11:13]
                minute = date_time[14:16]
                second = date_time[17:19]

                image = Image(year, month, day, hour, minute, second, path, filetype)

                return image

            if handle_nodate:
                move_or_copy_nodate(path)

            return False



    def get_year(self):
        return self.__year

    def get_month(self):
        return self.__month

    def get_day(self):
        return self.__day

    def get_hour(self):
        return self.__hour

    def get_minute(self):
        return self.__minute

    def get_second(self):
        return self.__second

    def get_path(self):
        return self.__path

    def get_filetype(self):
        return self.__filetype

help_text = '''Usage: p3m -src <UNSORTED IMAGES> -dst <PATH TO SORT IMAGES TO> [options]
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
'''

naming_help = '''Usage Naming Scheme: -n \"[VALUE][SEPERATOR][VALUE]\"
Values can be: YEAR, MONTH, DAY, HOUR, MINUTE, SECOND
Seperators can be any character or string except characters that confuse your os (/ , . , ~ , *)

Examples:                                   Result:
YEAR_MONTH_DAY_HOUR_MINUTE_SECOND           2012_21_12_13_37_00.JPG
image_DAY_MONTH_YEAR-HOUR:MINUTE:SECOND     image_12_21_2012-13:37:00.JPG

Keep in mind that the second example will result in your pictures not being arranged in the right order (sorted by recording date)
if viewed in a file browser that sorts them by name.
'''

sorting_help = '''Usage Sorting Scheme: -s \"[VALUE]/[VALUE]\"
Values can be: YEAR, MONTH, DAY, HOUR, MINUTE, SECOND or any string
Seperate your folders with a / like you would normally do
The first folder of your naming sceme will be located in the folder you specified as destination

Examples:                               Result:
YEAR/MONTH                              2012/12/image.JPG
images/YEAR/MONTH/DAY                   images/2012/12/21/image.JPG
'''

recursive = False
move = False
backup = False
confirmation = True
overrite_backup = False
overrite = False
source = ""
destination = ""
backup_destination = ""
naming_scheme = ""
sorting_scheme = ""
image_move_count = 0
handle_nodate = False
verbose = False
use_creation_date = False


# fallback if no metadata is found
# determine the date by the files creation date

def get_time_from_creation_date(path):
    # Get the creation date of the file
    # credits: Mark Amery and igacia @ https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    time = 0

    # Windows ?!
    if platform.system() == 'Windows':
        time = os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            time = stat.st_birthtime
        except AttributeError:
            # Linux?!
            time = stat.st_mtime
    
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def move_or_copy_nodate(image):
    os.makedirs(os.path.join(destination, "NoDate"), exist_ok=True)
    save_image(image, os.path.join(destination, "NoDate", image.split("/")[len(image.split("/")) - 1]))

def sort_images(files, path):
    if sorting_scheme == "":
        # if a name allready exists inkrement i until there is a file name that doesnt exist unless the user wishes to overrite files with duplicate names
        for image in files:
            i = 0
            if overrite == False:
                while os.path.isfile(os.path.join(path, determine_image_name(image, i))):
                    i += 1

            # just move or copy the image without creating any folders
            save_image(image.get_path(), os.path.join(path, determine_image_name(image, i)))
    else:
        for image in files:
            # create folder recursively
            os.makedirs(os.path.join(path, determine_folder_name(image)), exist_ok=True)

            # if a name allready exists inkrement i until there is a file name that doesnt exist unless the user wishes to overrite files with duplicate names
            i = 0
            if overrite == False:
                while os.path.isfile(os.path.join(path, determine_folder_name(image), determine_image_name(image, i))):
                    i += 1

            # move or copy the image
            save_image(image.get_path(), os.path.join(path, determine_folder_name(image), determine_image_name(image, i)))


def save_image(source, destination):
    global image_move_count
    if move:
        os.rename(source, destination)
        image_move_count += 1
        print("[ INFO ] Moved file from: " + bcolors.WARNING + source + bcolors.ENDC + " to " + bcolors.WARNING + destination + bcolors.ENDC)
    else:
        shutil.copy(source, destination)
        image_move_count += 1
        print("[ INFO ] Copied file from: " + bcolors.WARNING + source + bcolors.ENDC + " to " + bcolors.WARNING + destination + bcolors.ENDC)


def determine_folder_name(image):
    # determine image path by naming scheme
    folder_name = sorting_scheme.replace("YEAR", image.get_year())
    folder_name = folder_name.replace("MONTH", image.get_month())
    folder_name = folder_name.replace("DAY", image.get_day())
    folder_name = folder_name.replace("HOUR", image.get_hour())
    folder_name = folder_name.replace("MINUTE", image.get_minute())
    folder_name = folder_name.replace("SECOND", image.get_second())

    return folder_name


def preview_folder_name():

    temp_name = sorting_scheme.replace("YEAR", "2012")
    temp_name = temp_name.replace("MONTH", "12")
    temp_name = temp_name.replace("DAY", "21")
    temp_name = temp_name.replace("HOUR", "13")
    temp_name = temp_name.replace("MINUTE", "37")
    temp_name = temp_name.replace("SECOND", "00")

    return temp_name


def determine_image_name(image, number):

    if naming_scheme == "":
        if number == 0:
            return(os.path.split(image.get_path())[1].split(".")[0] + image.get_filetype())
        else:
            return(os.path.split(image.get_path())[1].split(".")[0] + "(" + str(number) + ")" + image.get_filetype())
    else:
        temp_name = naming_scheme.replace("YEAR", image.get_year())
        temp_name = temp_name.replace("MONTH", image.get_month())
        temp_name = temp_name.replace("DAY", image.get_day())
        temp_name = temp_name.replace("HOUR", image.get_hour())
        temp_name = temp_name.replace("MINUTE", image.get_minute())
        temp_name = temp_name.replace("SECOND", image.get_second())

        if number == 0:
            return temp_name + image.get_filetype()
        else:
            return temp_name + "(" + str(number) + ")" + image.get_filetype()


def preview_image_name():

    temp_name = naming_scheme.replace("YEAR", "2012")
    temp_name = temp_name.replace("MONTH", "12")
    temp_name = temp_name.replace("DAY", "21")
    temp_name = temp_name.replace("HOUR", "13")
    temp_name = temp_name.replace("MINUTE", "37")
    temp_name = temp_name.replace("SECOND", "00")

    return temp_name + ".JPG"

# scans through given folder (recursively if wanted) and creates a Image object for any image that contains exif information


def scan_folder(path):
    for filename in os.listdir(path):
        if filename.endswith(".JPG") or filename.endswith(".jpg") or filename.endswith(".JPEG") or filename.endswith(".jpeg") or filename.endswith(".MOV") or filename.endswith(".mov") or filename.endswith(".MP4") or filename.endswith(".mp4"):
            image = Image.create_image(os.path.join(path, filename))
            if image != False:
                file_list.append(image)
        elif os.path.isdir(os.path.join(path, filename)) and not recursive:
            print(bcolors.WARNING + "[ WARNING ] " + bcolors.ENDC + filename + bcolors.WARNING + " is a directory! Use -r to also sort subfolders. " + bcolors.ENDC)
        elif os.path.isdir(os.path.join(path, filename)) and recursive and os.path.join(path, filename) != os.path.abspath(destination):
            scan_folder(os.path.join(path, filename))
        elif os.path.isdir(os.path.abspath(destination)) and recursive and os.path.join(path, filename) == os.path.abspath(destination):
            print(bcolors.WARNING + "[ WARNING ] Skipped " + bcolors.ENDC + filename + bcolors.WARNING + " because it's the destination folder! " + bcolors.ENDC)
        elif use_creation_date:
            image = Image.create_image(os.path.join(path, filename))
            if image != False:
                file_list.append(image)
        else:
            print(bcolors.WARNING + "[ WARNING ] " + "Unsupported filetype " + filename[filename.find("."):len(filename)] + " for: " + bcolors.ENDC + filename)
            
            if handle_nodate:
                move_or_copy_nodate(os.path.join(path, filename))


def perform_backup(src_path, dst_path, overrite):
    if os.path.isdir(os.path.join(dst_path, "Backup")):
        if overrite and recursive:
            shutil.rmtree(os.path.join(dst_path, "Backup"))
            print("[ INFO ] Removed old Backup at: " + bcolors.WARNING + os.path.join(dst_path, "Backup") + bcolors.ENDC)
            shutil.copytree(src_path, os.path.join(dst_path, "Backup"))
        elif overrite and not recursive:
            shutil.rmtree(os.path.join(dst_path, "Backup"))
            print("[ INFO ] Removed old Backup at: " + bcolors.WARNING + os.path.join(dst_path, "Backup") + bcolors.ENDC)

            os.makedirs(os.path.join(dst_path, "Backup"))
            for filename in os.listdir(src_path):
                if not os.path.isdir(filename):
                    shutil.copyfile(os.path.join(src_path, filename), os.path.join(dst_path, "Backup", filename))
        else:
            print(bcolors.FAIL + "[ ERROR ] There is allready a backup at " + bcolors.ENDC + os.path.join(dst_path, "Backup") + bcolors.FAIL + " ! Delete the Backup folder or use -xB to overrite it.")
            sys.exit()
    else:
        if recursive:
            shutil.copytree(src_path, os.path.join(dst_path, "Backup"))
        else:
            os.makedirs(os.path.join(dst_path, "Backup"))
            for filename in os.listdir(src_path):
                if not os.path.isdir(filename):
                    print(os.path.join(src_path, filename))
                    shutil.copyfile(os.path.join(src_path, filename), os.path.join(dst_path, "Backup", filename))

    print("[ INFO ] Backup created at: " + os.path.join(dst_path, "Backup"))


# prints out a summary of the settings the user has set and asks for confirmation if not otherwise specified (-x)
def summarize():
    sys.stdout.write("[ INFO ] Images will be ")

    if move:
        sys.stdout.write(bcolors.WARNING + "moved" + bcolors.ENDC)
    else:
        sys.stdout.write(bcolors.WARNING + "copied" + bcolors.ENDC)

    sys.stdout.write(" from " + bcolors.WARNING + source + bcolors.ENDC)

    if recursive:
        sys.stdout.write(bcolors.WARNING + " INCLUDING SUBFOLDERS" + bcolors.ENDC)

    sys.stdout.write(" to " + bcolors.WARNING + destination + bcolors.ENDC + "!\n")
    sys.stdout.flush()

    if naming_scheme != "":
        sys.stdout.write("[ INFO ] The images will be named like this: " + bcolors.WARNING + preview_image_name() + bcolors.ENDC + "\n")

    if sorting_scheme != "":
        sys.stdout.write("[ INFO ] The folder structure in the destination folder will look like this: " + bcolors.WARNING + preview_folder_name() + bcolors.ENDC + "\n")

    if use_creation_date:
        sys.stdout.write("[ INFO ] The creation date of a file will be used as fallback if the metadata contains no information" + "\n")

    if handle_nodate:
        sys.stdout.write("[ INFO ] Images with a non determinable date will be ")
        if move:
            sys.stdout.write(bcolors.WARNING + "moved" + bcolors.ENDC)
        else:
            sys.stdout.write(bcolors.WARNING + "copied" + bcolors.ENDC)
        sys.stdout.write(" to " + bcolors.WARNING + os.path.join(destination, "NoDate") + bcolors.ENDC + "\n")
    else:
        sys.stdout.write("[ INFO ] Images with a non determinable date will not be touched!" + "\n")

    if backup:
        sys.stdout.write("[ INFO ] A backup will be created at: " + bcolors.WARNING + os.path.join(backup_destination, "Backup") + bcolors.ENDC + "\n")
    elif move:
        sys.stdout.write(bcolors.WARNING + "[ WARNING ] No backup will be created!" + bcolors.ENDC + "\n")

    if overrite_backup and backup:
        sys.stdout.write(bcolors.WARNING + "[ WARNING ] The old backup folder will be overritten!" + bcolors.ENDC + "\n")

    if overrite:
        sys.stdout.write(bcolors.WARNING + "[ WARNING ] Files with duplicate names will be overritten" + bcolors.ENDC + "\n")

    sys.stdout.flush()

    if confirmation:
        sys.stdout.write(bcolors.OKGREEN + "Do you want to proceed? (N) " + bcolors.ENDC)
        sys.stdout.flush()
        answare = sys.stdin.readline()
        if answare != "Y\n" and answare != "y\n" and answare != "yes\n" and answare != "Yes\n" and answare != "J\n" and answare != "j\n":
            print(bcolors.FAIL + "[ ABORTED ] Aborted by user!" + bcolors.ENDC)
            sys.exit()


# sets the script up according to the users input
def setup():
    global source
    global destination
    global move
    global backup
    global backup_destination
    global recursive
    global overrite_backup
    global confirmation
    global naming_scheme
    global sorting_scheme
    global overrite
    global handle_nodate
    global verbose
    global use_creation_date

    skipnextargument = False

    for index, argument in enumerate(sys.argv):
        # skip this argument because it is s sub argument
        if skipnextargument:
            skipnextargument = False
            continue

        if argument == "--naming" or argument == "-n":
            if len(sys.argv) == index + 1:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -n or --naming must be followed by the naming scheme!" + bcolors.ENDC)
                sys.exit()
            else:
                if not sys.argv[index + 1] == "--help" and not sys.argv[index + 1] == "-h":
                    naming_scheme = sys.argv[index + 1]
                    skipnextargument = True
                else:
                    print(naming_help)
                    sys.exit()
        elif argument == "--sorting" or argument == "-s":
            if len(sys.argv) == index + 1:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -s or --sorting must be followed by the sorting scheme!" + bcolors.ENDC)
                sys.exit()
            else:
                if not sys.argv[index + 1] == "--help" and not sys.argv[index + 1] == "-h":
                    sorting_scheme = sys.argv[index + 1]
                    skipnextargument = True
                else:
                    print(sorting_help)
                    sys.exit()
        elif argument == "--help" or argument == "-h":
            print(help_text)
            sys.exit()
        elif argument == "--recursive" or argument == "-r":
            recursive = True
        elif argument == "--move" or argument == "-m":
            move = True
        elif argument == "--source" or argument == "-src":
            if len(sys.argv) == index + 1:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -src or --source must be followed by a path!" + bcolors.ENDC)
                sys.exit()
            elif os.path.isdir(sys.argv[index + 1]):
                source = sys.argv[index + 1]
                skipnextargument = True
            else:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -src or --source must be followed by a path! " + bcolors.ENDC + sys.argv[index + 1] + bcolors.FAIL + " is not a path! " + bcolors.ENDC)
                sys.exit()
        elif argument == "--destination" or argument == "-dst":
            if len(sys.argv) == index + 1:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -dst or --destination must be followed by a path!" + bcolors.ENDC)
                sys.exit()
            elif os.path.isdir(sys.argv[index + 1]):
                destination = sys.argv[index + 1]
                skipnextargument = True
            else:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -dst or --destination must be followed by a path! " + bcolors.ENDC + sys.argv[index + 1] + bcolors.FAIL + " is not a path! " + bcolors.ENDC)
                sys.exit()
        elif argument == "--backup" or argument == "-b":
            if len(sys.argv) == index + 1:
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -b or --backup must be followed by a path!" + bcolors.ENDC)
                sys.exit()
            elif not os.path.isdir(sys.argv[index + 1]):
                print(bcolors.FAIL + "[ SYNTAX ERROR ] -b or --backup must be followed by a path! " + bcolors.ENDC + sys.argv[index + 1] + bcolors.FAIL + " is not a path! " + bcolors.ENDC)
                sys.exit()
            elif os.path.abspath(source) in os.path.abspath(sys.argv[index + 1]):
                print(bcolors.FAIL + "[ ERROR ] The backup folder can't be located in the source folder! This would result in a infinite loop and we would all die! Better fix that." + bcolors.ENDC)
                sys.exit()
            elif os.path.isdir(sys.argv[index + 1]):
                backup_destination = sys.argv[index + 1]
                backup = True
                skipnextargument = True
        elif argument == "-v"  or argument == "--verbose":
            verbose == True
        elif argument == "-a" or argument == "--handleNodate":
            handle_nodate = True
        elif argument == "-c" or argument == "--useCreationDate":
            use_creation_date = True
        elif argument == "-xB":
            overrite_backup = True
        elif argument == "-xC":
            confirmation = False
        elif argument == "-xO":
            overrite = True
        elif argument != sys.argv[0]:
            print(bcolors.FAIL + "[ ERROR ] Unknown argument: " + argument + "!" + bcolors.ENDC)
            sys.exit()
        

    # check if a source and a destination is given
    if source == "" or destination == "":
        print(bcolors.FAIL + "[ ERROR ] You have to at least provide a source and a destination path! Use --help for usage information." + bcolors.ENDC)
        sys.exit()


setup()

summarize()

if backup:
    perform_backup(source, backup_destination, overrite_backup)

# list of all images that contain exif information with timestamp
file_list = []

scan_folder(source)
sort_images(file_list, destination)
