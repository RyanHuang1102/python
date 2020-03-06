import ConfigParser
import fcntl
import json
import os
from time import sleep

MAX_TRY = 20
GET_LOCK_FILE_FAIL = -2

LUN_CONFIG = '/share/CACHEDEV1_DATA/.config/iscsi/qcs_iscsi_lun'
#Bitmap Control
CFG_LUNBitMap = 'LUNBitMap'

class INI_CONF():
    def __init__(self, config_path):
        parser = ConfigParser.RawConfigParser()
        self.config_path = config_path+'.ini'
        self.parser = parser
        self.parser.optionxform = str #prevent from string to lowercase
        if not os.path.isfile(self.config_path):#Default Conf
            path = os.path.split(config_path)[0]
            try:
                os.makedirs(path)
            except:
                pass
            finally:
                parser.add_section('Global')
                parser.set('Global', 'LogFlags', '7') 
                self.INI_Write_Conf(self.config_path)
                
    def Ini_Conf_Set_Field(self, section, field, field_data):
        lck_fo = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lck_fo, self.config_path)
            return -1

        if lck_fo is -1:
            return GET_LOCK_FILE_FAIL

        self.set_field(section, field, field_data)
        FILE_UNLOCK(lck_fo, self.config_path)
        return 0

    def Ini_Conf_Get_Field(self, section, field):
        lck_fo = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lck_fo, self.config_path)
            return -1

        if lck_fo is -1:
            return GET_LOCK_FILE_FAIL

        try:
            field_data = self.parser.get(section, field)
        except:
            FILE_UNLOCK(lck_fo, self.config_path)
            return -1 #section or field not exist

        FILE_UNLOCK(lck_fo, self.config_path)
        return field_data

    def Ini_Conf_Remove_Section(self, section):
        lck_fo = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lck_fo, self.config_path)
            return -1

        if lck_fo is -1:
            return GET_LOCK_FILE_FAIL

        #Section still can be removed which doesn't exist
        self.parser.remove_section(section)
        self.INI_Write_Conf(self.config_path)

        FILE_UNLOCK(lck_fo, self.config_path)
        return 0

    def INI_Write_Conf(self, config_path):
        fo = open(config_path, 'wb')
        self.parser.write(fo)
        fo.close()

    def set_field(self, section, field, field_data):
        try:
            self.parser.add_section(section) # new section
        except:
            pass #except:section existed, didn't add.
        finally:
            self.parser.set(section, field, str(field_data))
            self.INI_Write_Conf(self.config_path)

class JSON_CONF():
    def __init__(self, config_path):
        self.config_path = config_path+'.json'
        if not os.path.isfile(self.config_path):#Default Conf
            path = os.path.split(config_path)[0]
            try:
                os.makedirs(path)
            except:
                pass
            finally:
                dic = {'Global':{'LogFlags':'7'}}
        	fo = open(self.config_path, 'wb')
        	json.dump(dic, fo, indent = 2, sort_keys=True)
        	fo.close()

    def JSON_Write_Conf(self, data):
        if os.path.isfile(self.config_path):
            file_data = self.JSON_Read_Conf()
            file_data.update(data) #append new section

        lck_fo = FILE_LOCK(self.config_path)

        if lck_fo is -1:
            return GET_LOCK_FILE_FAIL

        fo = open(self.config_path, 'wb')
        json.dump(file_data, fo, indent = 2, sort_keys=True)
        fo.close()

        FILE_UNLOCK(lck_fo, self.config_path)
        return 0

    def JSON_Read_Conf(self):
        lck_fo = FILE_LOCK(self.config_path)

        if lck_fo is -1:
            return GET_LOCK_FILE_FAIL

        fo = open(self.config_path, 'r')
        data = json.load(fo)
        fo.close()

        FILE_UNLOCK(lck_fo, self.config_path)

        return data

def FILE_LOCK(path):
    fo = open(path+'.lck','wb')

    TRY = 0
    while(TRY < MAX_TRY):
        try:
            fcntl.flock(fo, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except:
            TRY+=1
            sleep(0.5)
    if (TRY == MAX_TRY):
        return -1 #Times Out !!

    return fo

def FILE_UNLOCK(fo, path):
    fcntl.flock(fo, fcntl.LOCK_UN)
    fo.close()
    try:
        os.unlink(path+'.lck')
    except:
        pass #unlink fail: it means that file is unlocked.
