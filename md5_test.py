import hashlib
import os


def calculate_md5(source):

    if os.path.isfile(source):
        print("test 1")
        hash_func = hashlib.new("md5")
        with open(source, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    if os.path.isdir(source):
        md5_dir = hashlib.md5()
        for file in source: 
            md5_dir.update(b'file')
    return md5_dir.hexdigest()  

print(calculate_md5("C:\\Users\\local_user\\Downloads\\test_folder\\main.py"))
#print(calculate_md5("C:\\Users\\local_user\\Downloads\\test_folder"))