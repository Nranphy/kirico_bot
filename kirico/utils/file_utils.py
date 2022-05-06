import os
import time




def check_dir(path:str):
    '''
    创建 不存在的文件夹.
    '''
    if not os.path.isdir(path):
        os.makedirs(path)
        return True
    return False

def check_file(path:str):
    '''
    创建 已存在目录 下不存在的文件.
    '''
    if not os.path.isfile(path):
        f = os.open(path,os.O_CREAT)
        os.close(f)
        return True
    return False

def rm_path(path:str):
    '''
    删除文件或目录，可删除非空目录.
    '''
    if (os.path.isdir(path)):
        for file in os.listdir(path):
            rm_path((os.path.join(path,file)))
        if (os.path.exists(path)):
            os.rmdir(path)
    else:
        if (os.path.exists(path)):
            os.remove(path)


def get_date_and_time() -> list:
    '''返回kirico标准化当前日期与时间。
    :返回含有标准化日期(str)和时间(str)的列表。
    '''
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date_str = time_str[:10]
    time_str = time_str[11:]
    return [date_str, time_str]