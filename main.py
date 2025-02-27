import errno
import shutil
import os
import time
import logging
from datetime import datetime
import sys


def main():

    #interval = int(input("Enter synchronization interval in seconds: "))
    #src_folder = "C:\\Users\\gabri\\learn to code\\python\\replica_project\\demo"
    #r_folder = "C:\\Users\\gabri\\learn to code\\python\\replica_project\\replica"
    try:
        interval = int(sys.argv[1])
        src_folder = sys.argv[2]
        r_folder = sys.argv[3]
    except Exception:
        print("Error while starting the script.")
        sys.exit
        
#    src_folder = "C:\\Users\\local_user\\Downloads\\Source"
#    r_folder = "C:\\Users\\local_user\\Downloads\\Replica"

    if not os.path.exists(src_folder):
        os.makedirs(src_folder)

    times = 5
    while times > 0:
        replica_func(src_folder, r_folder)
        time.sleep(interval)
        if times == 1:
            print()
            answer = input("Continue with the script? (Y/N)")
            if(answer.lower() == "y"):
                times = 5
            else: 
                break
        else:
            times -= 1

def replica_func(src, dest):
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='replica_logger.log', encoding='utf-8', level=logging.DEBUG)
    message = str(datetime.now()) + ' ' + 'Copied.'
    logger.info(message)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    
    if(os.path.isdir(dest)):
        shutil.rmtree(dest)
 
    try:
        shutil.copytree(src, dest)
#        print("successfully copied.")
    except OSError as exc: 
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dest)
        else: raise

main()
    