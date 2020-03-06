import ConfigParser
import fcntl
import os
from cfg_iscsi_defined import *
from err_trace import *
from time import sleep

class config():
    def __init__(self, config_path):
        parser = ConfigParser.RawConfigParser()
        self.config_path = config_path
        self.parser = parser
        if not os.path.isfile(self.config_path):#Default Conf
            path = os.path.split(config_path)
            try:
                os.makedirs(path)
            except:
                pass
            finally:
                fo = open(self.config_path, 'wb')
                parser.add_section('Global')
                parser.set('Global', 'LogFlags', '7') 
                parser.write(fo)
                fo.close()

    def set_field(self, section, field, field_data):
        try:
            self.parser.add_section(section) # new section
        except:
            pass #except:section existed, didn't add.
        finally:
            self.parser.set(section, field, str(field_data))
            fo = open(self.config_path, 'wb')
            self.parser.write(fo)
            fo.close()
                
    def Ini_Conf_Set_Field(self, section, field, field_data):
        lock_fo = FILE_LOCK(self.config_path)
        print section,field,field_data

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lock_fo, self.config_path)
            return -1

        if lock_fo is -1:
            return GET_LOCK_FILE_FAIL

        self.set_field(section, field, field_data)
        FILE_UNLOCK(lock_fo, self.config_path)
        return 0

    def Ini_Conf_Get_Field(self, section, field):
        lock_fo = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lock_fo, self.config_path)
            return -1

        if lock_fo is -1:
            return GET_LOCK_FILE_FAIL

        try:
            field_data = self.parser.get(section, field)
        except:
            FILE_UNLOCK(lock_fo, self.config_path)
            return -1 #section or field not exist

        FILE_UNLOCK(lock_fo, self.config_path)
        return field_data

    def Ini_Conf_Remove_Section(self, section):
        lock_fo = FILE_LOCK(self.config_path)

        if (self.parser.read(self.config_path) == []):
            FILE_UNLOCK(lock_fo, self.config_path)
            return -1

        if lock_fo is -1:
            return GET_LOCK_FILE_FAIL

        #Section still can be removed which doesn't exist
        self.parser.remove_section(section)
        fo = open(self.config_path, 'wb')
        self.parser.write(fo)
        fo.close()

        FILE_UNLOCK(lock_fo, self.config_path)
        return 0
        
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

def UINT_TEST_BIT(bit, pos):
    return bit & (0x00000001 << (pos))

def UINT_SET_BIT(bit, pos):
    bit |= (0x00000001 << (pos))
    return bit
"""
Target Control
"""
def CFG_Add_Target_Info(target_name, target_alias):
    target_name = str(target_name).lower()
    CONF = config(TARGET_FILE)
    
    ret, idx = acquire_idx_by_bmp_tag(TARGET_FILE, CFG_GLOBAL, CFG_TARGET_BITMAP, 8)
    if ret is -1:
        return ret

    target_section = CFG_TARGET_INFOI%idx
    target_iqn = targetIQNPrefix+target_name
    trgt_key = CFG_TARGET_INFOK+target_name

    #CONF.Ini_Conf_Set_Field(CFG_TARGET_KEY_SEC, CFG_TARGET_INFOK+target_iqn, idx)
    CONF.Ini_Conf_Set_Field(CFG_TARGET_KEY_SEC, trgt_key, idx)
    CONF.Ini_Conf_Set_Field(target_section, CFG_TARGET_INDEX, idx)
    CONF.Ini_Conf_Set_Field(target_section, CFG_TARGET_NAME, target_name)
    CONF.Ini_Conf_Set_Field(target_section, CFG_TARGET_IQN, target_iqn)
    CONF.Ini_Conf_Set_Field(target_section, CFG_TARGET_ALIAS, target_alias)
    CONF.Ini_Conf_Set_Field(target_section, CFG_TARGET_STATUS, TARGET_READY) 

    mesg = "CFG_Add_Target_Info:targetIndex=%(targetIndex)s targetIQN=%(targetIQN)s"
    dic = {CFG_TARGET_INDEX:idx, CFG_TARGET_IQN:target_iqn}
    ERR_TRACE('iscsi_lib.log', TARGET_FILE, TRACE_ENTRY, mesg%dic)

    return idx

def acquire_idx_by_bmp_tag(file_path, section, tag, max_bmp_idx):
    CONF = config(file_path)
    for bmp_idx in range(0, max_bmp_idx):
        bmp_name = tag+str(bmp_idx)
        ret = CONF.Ini_Conf_Get_Field(section, bmp_name)

        if ret is GET_LOCK_FILE_FAIL:
            ERR_TRACE('iscsi_lib.log', file_path, TRACE_ERROR, "acquire_idx_by_bmp_tag:times out to get lock")
            return -1, -1

        if ret is -1: #there is no this section, set initial value 0
            tag_value = 0
        else:
            tag_value = int(ret, 16)
        
        ret, idx = found_an_empty_slot(tag_value)
        if ret is 1: # founded empty slot
            tag_value = UINT_SET_BIT(tag_value, idx)
            if CONF.Ini_Conf_Set_Field(section, bmp_name, hex(tag_value)) is 0:
                idx += bmp_idx * MAX_IDX_BMP_SIZE
                break
    if ret is 0:
        ERR_TRACE('iscsi_lib.log', file_path, TRACE_ERROR, "acquire_idx_by_bmp_tag:no any places can be added")
        return -1, -1

    ERR_TRACE('iscsi_lib.log', file_path, TRACE_ENTRY, "acquire_idx_by_bmp_tag:tag=%(tag)s ret=%(ret)s idx=%(idx)s"%{'tag':tag, 'ret':ret, 'idx':idx})
    return ret, idx

def found_an_empty_slot(bitmap):
    ret = 0 
    for idx in range(0, MAX_IDX_BMP_SIZE):
        if UINT_TEST_BIT(bitmap, idx) is 0:
            ret = 1
            break
    return ret, idx
