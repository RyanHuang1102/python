import ConfigParser
import fcntl
from time import sleep
import os
from include.cfg_iscsi_define import *

class config():
    def __init__(self, config_path):
        parser = ConfigParser.SafeConfigParser()
        self.config_path = config_path
        self.parser = parser

    def set_field(self, section, field, fied_data):
        try:
            self.parser.add_section(section) # new section
            #sleep(10)
            #print "sleep10"
        except:
            pass #except: means section existed
        finally:
            self.parser.set(section, field, fied_data)
            self.parser.write(open(self.config_path, 'wb'))
                
    def Ini_Conf_Set_Field(self, section, field, fied_data):
        lock_fd = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []): #Defult Config
            self.parser.add_section('Global')
            self.parser.set('Global', 'LogFlags', '7') 
            if (self.config_path == TARGET_FILE):
                self.parser.set('Global', 'targetBitmap')
                pass
            elif (self.config_path == INITIATOR_FILE):
                pass
            elif (self.config_path == LUN_FILE):
                pass
            else:
                pass #Do Nothing 
            self.parser.write(open(self.config_path, 'wb'))

        self.set_field(section, field, fied_data)
        FILE_UNLOCK(lock_fd, self.config_path)
        return 0

    def Ini_Conf_Get_Field(self, section, field):
        lock_fd = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            print "config doesn't exist"
            FILE_UNLOCK(lock_fd, self.config_path)
            return -1

        try:
            field_data = self.parser.get(section, field)
        except:
            print "Please check section or field"
            FILE_UNLOCK(lock_fd, self.config_path)
            return -1

        FILE_UNLOCK(lock_fd, self.config_path)
        return field_data

    def Ini_Conf_Remove_Section(self, section):
        lock_fd = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            print "config doesn't exist"
            FILE_UNLOCK(lock_fd, self.config_path)
            return -1
        #Section still can be removed which doesn't exist
        self.parser.remove_section(section)
        self.parser.write(open(self.config_path, 'wb'))

        FILE_UNLOCK(lock_fd, self.config_path)
        return 0
        
def FILE_LOCK(path):
    fd = open(path+'.lck','wb')
    TRY = 0
    while(TRY < MAX_TRY):
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except:
            TRY+=1
            sleep(0.5)
            print TRY
    if (TRY == MAX_TRY):
        print "Times Out, File Locked"
        return -1
    return fd

def FILE_UNLOCK(fd, path):
    try:
        os.unlink(path+'.lck')
    except:
        pass #unlink fail: it means that file is unlocked.
    fcntl.flock(fd, fcntl.LOCK_UN)
    return

"""
Bit operation
"""

def UINT_TEST_BIT(bit, pos):
    return (bit & (0x00000001 << (pos)))

def UINT_TEST_BIT(bit, pos):
    bit |= (0x00000001 << (pos))
    return bit

def found_an_empty_slot(bitmap):
    ret = 0 
    for idx in range(0, MAX_IDX_BMP_SIZE):
        if UINT_TEST_BIT(bitmap, idx) is 0:
            ret = 1
            break
    return ret, idx

"""
ret, idx = found_an_empty_slot(00000000)

print ret, idx
"""
