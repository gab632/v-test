import errno
import shutil
import os
import time
import logging
from datetime import datetime
import sys
import hashlib
import traceback

def main():

    try:
        src_folder = sys.argv[1]
        r_folder = sys.argv[2]
        log_file_path = sys.argv[3]
        interval = int(sys.argv[4])

    except Exception:
        print("Error while starting the script.")
        sys.exit()

    create_folders_and_log_file(src_folder, r_folder, log_file_path)

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)

    while True:     
        replica_func(src_folder, r_folder, logger)
        time.sleep(interval)

# copy the content of src folder into dest folder.
def replica_func(src, dest, logger):

    try:
        # copy the file if it is not in the replica folder
        for file in os.listdir(src):
            os.chdir(src)
            file_path = os.getcwd() + '\\' + file
            if not file in os.listdir(dest):

                shutil.copy2(file_path, dest)
                # log the operation
                message = str(datetime.now())  + ' File \"' + file + '\" copied.'
                logger.debug(message)
            else: 
                src_file_last_modified = os.path.getmtime(file_path)
                os.chdir(dest)
                dest_file_path = os.getcwd() + '\\' + file
                dest_file_last_modified = os.path.getmtime(dest_file_path)
                if not src_file_last_modified == dest_file_last_modified:
                    shutil.copy2(file_path, dest)
                    message = str(datetime.now()) + ' File \"' + file + '\" modified.'
                    logger.debug(message)
        # remove the file if it is no longer in the source folder.
        for file in os.listdir(dest):
            if not file in os.listdir(src):
                os.chdir(dest)
                file_path = os.getcwd() + '\\' + file
                os.remove(file_path)  
                message = str(datetime.now()) + ' File \"' + file + '\" removed.'
                logger.debug(message)

#        shutil.copytree(src, dest, dirs_exist_ok=True)
#        message = str(datetime.now()) + ' ' + 'Copied.'
#        logger.debug(message)
    except OSError as exc: 
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dest)
        else: 
            traceback.print_exc()
    #console.close()
    
    
# create two folders if they do not exist.
# create a file given the file path.
def create_folders_and_log_file(folder1, folder2, file_path):
    try:
        if not os.path.exists(folder1):
            os.makedirs(folder1)

        if not os.path.exists(folder2):
            os.makedirs(folder2)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    except OSError as exc:
        print("Error while creating folders and log file.")
        print(exc)
        sys.exit()

# hashing function for both files and folders
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

main()
    