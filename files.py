#Код для работы с файлами
import os
import shutil
def file_exists(str):
    if os.path.exists(str):
        if os.path.isfile(str):
            return True
        else:
            return False
    else:
        return False
def file_read(str):
    #Вызывает исключения: FileNotFoundError
    if file_exists(str):
        f = open(str, "r")
        result = f.read()
        f.close()
        return result
    else:
        raise FileNotFoundError()
def file_write(str, content=None):
    if file_exists(str):
        f = open(str, "w")
        f.write(content)
        f.close()
    else:
        f = open(str, "c")
        f.write(content)
        f.close()
def file_delete(str):
    #Вызывает исключения: FileNotFoundError, PermissionError
    os.remove(str)
#Код для работы с папками
def dir_exists(str):
    if os.path.exists(str):
        if os.path.isdir(str):
            return True
        else:
            return False
    else:
        return False
def dir_create(str):
    #Вызывает исключения: FileExistsError, PermissionError, OSError
    os.mkdir(str)
def dir_delete(str):
    #Вызывает исключения: FileNotFoundError, PermissionError, OSError
    os.rmdir(str)
def tree_delete(str):
    shutil.rmtree(str)