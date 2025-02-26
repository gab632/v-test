
import errno
import shutil
import os
import time
import logging
from datetime import datetime

def main():

    interval = int(input("Enter synchronization interval in seconds: "))

    def replica_func(src, dest):
        

        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='replica_logger.log', encoding='utf-8', level=logging.DEBUG)
        logger.info(datetime.now())

        if(os.path.isdir(dest)):
            shutil.rmtree(dest)

        try:
            shutil.copytree(src, dest)
            print("successfully copied.")
        except OSError as exc: # python >2.5
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(src, dest)
            else: raise

    src_folder = "C:\\Users\\gabri\\learn to code\\python\\replica_project\\demo"
    r_folder = "C:\\Users\\gabri\\learn to code\\python\\replica_project\\replica"

    times = 5
    while times > 0:
        replica_func(src_folder, r_folder)
        time.sleep(interval)
        if times == 1:
            print()
            answer = input("Continue with the script? (Y/N)")
            if(answer == "y" or answer == "Y"):
                times = 10
            else: 
                break
        else:
            times -= 1

    
    def is_os_windows():
        pass

    
def add_backslash(string):
        new_string = ""
        for c in string:
            if c == "\\":
                new_string += "\\\\"
            else: 
                new_string += c
        return new_string

main()

    