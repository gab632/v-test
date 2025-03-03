import shutil
import os
import time
import logging
from datetime import datetime
import sys
import hashlib

def main():

    # input from command line - order of arguments: 
    # 1. source folder absolute path,
    # 2. replica folder absolute path,
    # 3. log file path,
    # 4. interval value (in seconds)    
    try: 
        src_folder = sys.argv[1]
        r_folder = sys.argv[2]
        log_file_path = sys.argv[3]
        interval = int(sys.argv[4])

    except Exception as exc:
        print("Error while starting the script.")
        print(exc)
        sys.exit()

    abs_file_path = create_absolute_file_path(log_file_path)
    create_folders_and_log_file(src_folder, r_folder, abs_file_path)

    logger = initialize_logger(abs_file_path)
    
    # runs until external command (i.e. ctrl+c) breaks the loop.
    while True:     
        replica_func(src_folder, r_folder, logger)
        time.sleep(interval)


# copy the content of src folder into dest folder.
# logs using the paramenter logger. 
# returns none.
def replica_func(src, dest, logger):

    try:
        # copy the file if it is not in the replica folder
        for file in os.listdir(src):
            os.chdir(src)
            file_path = os.getcwd() + '\\' + file
            if not file in os.listdir(dest):
                shutil.copy2(file_path, dest)

                # log the file creation.
                message = str(datetime.now())  + ' File \"' + file + '\" copied.'
                logger.debug(message)
            else: 
                # if file has been modified, copy the new version. 
                # file modification = content modification. 
                src_file_last_modified = os.path.getmtime(file_path)
                os.chdir(dest)
                dest_file_path = os.getcwd() + '\\' + file
                dest_file_last_modified = os.path.getmtime(dest_file_path)
                if not src_file_last_modified == dest_file_last_modified:
                    shutil.copy2(file_path, dest)

                    # log the file modification. 
                    message = str(datetime.now()) + ' File \"' + file + '\" modified.'
                    logger.debug(message)
        # remove the file if it is no longer in the source folder.
        for file in os.listdir(dest):
            # file removal code.    
            if not file in os.listdir(src):
                os.chdir(dest)
                file_path = os.getcwd() + '\\' + file
                os.remove(file_path)  
                
                # log the file removal.
                message = str(datetime.now()) + ' File \"' + file + '\" removed.'
                logger.debug(message)

    except OSError as exc: 
        print("Error during copy/modification/removal operation.")
        print(exc)
        sys.exit()
    

# create two folders if they do not exist.
# create a file given the file path.
# returns none
def create_folders_and_log_file(folder1, folder2, file_path):
    try:
        if not os.path.exists(folder1):
            os.makedirs(folder1)

        if not os.path.exists(folder2):
            os.makedirs(folder2)

        if os.path.isabs(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        else: 
            abs_file_path = os.getcwd() + '\\logs\\' + file_path
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
    except OSError as exc:
        print("Error while creating folders and log file.")
        print(exc)
        sys.exit()


# hashing function for both files and folders.
# NOTE: I took the original base code of this hash function from a stackoverflow thread. 
#       Then I tested and modified the code for my purpose. 
# returns a string representing the hexadecimal number of the hash result  
def calculate_md5(source):

    hash_func = hashlib.new("md5")

    if os.path.isfile(source):
        file_name = os.getcwd() + '\\' + source
        b = file_name.encode('utf-8')
        hash_func.update(b)

        with open(source, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    
    if os.path.isdir(source):
        os.chdir(source)

        for file in os.listdir(source): 
            file_name = os.getcwd() + '\\' + file
            b = file_name.encode('utf-8')
            hash_func.update(b)
            with open(file, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)

    return hash_func.hexdigest()  


# creates a logger object.
# adds a console log stream. 
# NOTE: for some lines of code ("how to log to the console"), 
#       I used a chatGPT reply, 
#       and then I tested and modified the chatGPT code for my purpose. 
# returns a logger object
def initialize_logger(log_file_path):
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)
    return logger

def create_absolute_file_path(file_path):
    try:
        if os.path.isabs(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            return file_path
        else: 
            abs_file_path = os.getcwd() + '\\logs\\' + file_path
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            return abs_file_path
        
    except OSError as exc:
        print("error while creating the file absolute path")
        print(exc)
    
main()
    