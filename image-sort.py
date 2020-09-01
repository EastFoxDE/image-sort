#!/usr/bin/env python3
import os
import shutil
import configparser
import getpass
os.system("clear") #clear console-screen

#read the config and set variables
config = configparser.ConfigParser()
config.read('settings.conf')

path = config['DEFAULT']['source_dir'] 
path = path.replace("username", getpass.getuser()) #input directory

count_jpg = 0
count_error = 0
list_error = [] 

#WELCOME-PROMPT and changing of variables
print("Welcome to my image-filter-tool!", config['EASTFOXES']['version'],"\nPlease make sure to read the readme.rtf before you continue\n")
print("In which folder are the files located?\nCurrent set source path is :", path)
path = path + input(".../")
path_ext = path + config['DEFAULT']['working_dir'] #output directory

try: 
    list = os.listdir(path) #Read all files from input directory
except:
    print("\n...source directory could not be found. Exiting the script.\n")
    quit()

#Creating the dest. directory, if not present
print("\n... creating destination directory")
try:
    os.makedirs(path_ext)
except:
    print("... destination directory already exists or not allowed to create directory")    

#Go trough every file from the directory and check if there's a "jpg" in the filename
print("... starting the filtering and copying of the files")
for object in list:    
    if ".JPG" in object:
        count_jpg += 1
        #create destination-filename
        file = object.replace("JPG", "NEF")
        #set source-file and destination-file
        source = path + "/" + file
        target = path_ext + "/" + file

        try:
            shutil.copy(source, target)
            
        except IOError as e:
            list_error.append("Unable to copy file. %s" % e)
            count_error += 1
        except:
            list_error.append("Unexpected error:", sys.exc_info())
            count_error += 1

#Giving the user a report about the script-run
print("\nAll objects in the list were filtered. \nThe script found", count_jpg, "JPG-files.")
#Outputs a message if any file-errors occured
if count_error > 0:
    print("\nThere were", count_error, "NEF-files which COULDNT BE copied. \nPlease check if all files are avaiable and the directory (", path_ext, ") is not write-protected.")
    
    if 'yes' in config['DEFAULT']['file_debug']: #outputs all error-messages if debugging is set to 'yes'
        for error in list_error:
            print(error)
        
if 'yes' in config['DEFAULT']['extended_debug']: #outputs all important variables with its values
    print("\nsource_path:", path)
    print("working_path:", path_ext)
    print("count_jpg:", count_jpg)
    print("count_error:", count_error)
    #print("all found files:", list)

print("")

#fin