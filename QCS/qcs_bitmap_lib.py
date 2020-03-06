from qcs_iscsi_lib import *
from qcs_iscsi_config import *

def UINT_TEST_BIT(bit, pos):
    return bit & (0x00000001 << (pos))

def UINT_SET_BIT(bit, pos):
    bit |= (0x00000001 << (pos))
    return bit

def acquire_idx_by_bmp_tag(file_path, section, tag, max_bmp_idx):
    CONF = JSON_CONF(file_path)
    for bmp_idx in range(0, max_bmp_idx):
        bmp_name = tag+str(bmp_idx)
        data = CONF.JSON_Read_Conf()

        if data is GET_LOCK_FILE_FAIL:
            ERR_TRACE(TRACE_ERROR, "ret:%d acquire_idx_by_bmp_tag:times out to get lock"%(ret))
            return GET_LOCK_FILE_FAIL
        try:
            tag_value = int(data[section][bmp_name], 16)
        except 
            tag_value = 0 #default value
        
        ret, idx = found_an_empty_slot(tag_value)
        if ret is 1: # founded empty slot
            tag_value = UINT_SET_BIT(tag_value, idx)
            data[section][bmp_name] = hex(tag_value)
            if CONF.JSON_Write_Conf(data) is 0:
                idx += bmp_idx * MAX_IDX_BMP_SIZE
                break
    if ret is 0:
        ERR_TRACE(TRACE_ERROR, "acquire_idx_by_bmp_tag:no any places can be added")
        return -1, -1

    ERR_TRACE(TRACE_ENTRY, "acquire_idx_by_bmp_tag:tag=%(tag)s ret=%(ret)s idx=%(idx)s"%{'tag':bmp_name, 'ret':ret, 'idx':idx})
    return ret, idx

def found_an_empty_slot(bitmap):
    ret = 0 
    for idx in range(0, MAX_IDX_BMP_SIZE):
        if UINT_TEST_BIT(bitmap, idx) is 0:
            ret = 1
            break
    return ret, idx
