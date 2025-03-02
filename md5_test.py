import hashlib
import os


def calculate_md5(source):

    hash_func = hashlib.new("md5")

    if os.path.isfile(source):       
        with open(source, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)

        return hash_func.hexdigest()
    
    if os.path.isdir(source):
        os.chdir(source)
#        md5_dir = hashlib.md5()
        for file in os.listdir(source): 
           
            with open(file, 'rb') as f:
                while chunk := f.read(8192):
                    hash_func.update(chunk)
        
    return hash_func.hexdigest()  


print(calculate_md5("C:\\Users\\gabri\\Downloads\\Test"))
#print(calculate_md5("C:\\Users\\local_user\\Downloads\\test_folder"))