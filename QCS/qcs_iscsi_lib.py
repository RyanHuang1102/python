import logging
import ConfigParser
import os
from logging.handlers import RotatingFileHandler
from qcs_utils import cmd_utils

#TRACE CTRL
TRACE_ERROR = 0x0001
TRACE_WARNING = 0x0002
TRACE_ENTRY = 0x0004

#CEPH UTIL CTRL
CEPH_UTIL_PATH = "/usr/local/ceph"

#RBD CMD CTRL
ID_KEYRING = " --id %s --keyring=/etc/ceph/ceph.client.%s.keyring"
CMD_RBD = CEPH_UTIL_PATH+"/bin/rbd"
RBD_GET_INFO = CMD_RBD+" info --pool %s --image %s --format json"+ID_KEYRING
RBD_GET_DEVICE_INFO = CMD_RBD+" device list --format json"+ID_KEYRING

RBD_CREATE_IMAGE = CMD_RBD+" create --size %s --pool %s --image %s --image-feature layering"+ID_KEYRING #default thin image
RBD_CREATE_THICK_IMAGE = CMD_RBD+" create --size %s --pool %s --image %s --image-feature layering --thick-provision"+ID_KEYRING

RBD_REMOVE_IMAGE = CMD_RBD+" remove --pool %s --image %s"+ID_KEYRING

RBD_MAP_DEVICE = CMD_RBD+" map --pool %s --image %s"+ID_KEYRING
RBD_UNMAP_DEVICE = CMD_RBD+" unmap --pool %s --image %s"+ID_KEYRING

RBD_RESIZE_IMAGE = CMD_RBD+" resize --pool %s --image %s --size %s"
RBD_RENAME_IMAGE = CMD_RBD+" rename --pool %s --image %s %s"

#RETURN CONTROL
IMAGE_EXISTED = 1
#GET ENV
pool = os.getenv('CLUSTER')#ceph_pool name is identical to cluster_name, when create a cluster. 

def qcs_create_disk(disk_size, lun_name):
    ret = _check_rbd_image_exist(pool, lun_name)
    if ret is 0: # image exist
        ret, dev = qcs_get_rbd_device(lun_name)
        ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_create_disk: image existed, dev=%s"%(ret, dev))
    else:
        ret = _qcs_create_rbd_image(disk_size, pool, lun_name)
        if ret is 0:
           ret, dev = _qcs_map_rbd_to_device(pool, lun_name)

    return ret, dev

def _qcs_create_rbd_image(disk_size, pool_name, lun_name):
    cmd = RBD_CREATE_IMAGE %(disk_size, pool_name, lun_name, pool_name, pool_name)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_create_rbd_image:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def _qcs_map_rbd_to_device(pool_name, lun_name):
    cmd = RBD_MAP_DEVICE %(pool_name, lun_name, pool_name, pool_name)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_map_rbd_to_device:%s dev:%s"%(ret['return_code'], cmd, ret['json_output'][0]['raw_data']))
    return ret['return_code'], ret['json_output'][0]['raw_data']
 
def _check_rbd_image_exist(pool_name, lun_name):
    ret = cmd_utils(RBD_GET_INFO %(pool_name, lun_name, pool_name, pool_name)).check_output()
    return ret['return_code']

def qcs_get_rbd_device(lun_name):
    data = _get_rbd_device()
    for i in range(len(data)):
        if data[i]['name'] == lun_name:
            return 0, data[i]['device']

def _get_rbd_device():
    cmd = RBD_GET_DEVICE_INFO %(pool, pool)
    ret = cmd_utils(cmd).check_output()
    return ret['json_output']

def qcs_remove_disk(lun_name):
    ret = _check_rbd_image_exist(pool, lun_name)
    if ret is 0:
        ret = _qcs_unmap_rbd_from_device(pool, lun_name)
        _qcs_remove_rbd_image(pool, lun_name)
        ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_remove_disk: remove successfully."%(ret))
    return ret

def _qcs_remove_rbd_image(pool_name, lun_name):
    cmd = RBD_REMOVE_IMAGE %(pool_name, lun_name, pool_name, pool_name)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_remove_rbd_image:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def _qcs_unmap_rbd_from_device(pool_name, lun_name):
    cmd = RBD_UNMAP_DEVICE %(pool_name, lun_name, pool_name, pool_name) 
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_unmap_rbd_from_device:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_resize_lun(disk_size, lun_name):
    cmd = RBD_RESIZE_IMAGE %(pool, lun_name, disk_size)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_resize_lun:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_rename_image(old_name, new_name):
    cmd = RBD_RENAME_IMAGE %(pool, old_name, new_name)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_rename_image:%s"%(ret['return_code'], cmd))
    return ret['return_code']

#1 Mbytes
def ERR_TRACE(level, string):
    log_path='/share/CACHEDEV1_DATA/log/iscsi/qcs_iscsi_service.log'

    if not os.path.isfile(log_path):
        path = os.path.split(log_path)[0]
        try:
            os.makedirs(path)
        except:
            pass

    handler = RotatingFileHandler(log_path, mode='w', maxBytes = 1024*1024, backupCount = 1)
    formatter = logging.Formatter(fmt = '%(asctime)s %(name)-12s %(levelname)s %(message)s', datefmt = '[%Y/%m/%d %H:%M:%S]')
    handler.setFormatter(formatter)

    logger = logging.getLogger('qcs_iscsi_lib')
    if not logger.handlers: # prevent from adding handlers
        logger.addHandler(handler)

    if (level == TRACE_ERROR):
        logger.setLevel(logging.ERROR)
        logger.error(string)
    elif (level == TRACE_WARNING):
        logger.setLevel(logging.WARNING)
        logger.warning(string)
    elif (level == TRACE_ENTRY):
        logger.setLevel(logging.INFO)
        logger.info(string)
    else:
        return #do nothing
