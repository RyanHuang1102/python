import ConfigParser
import os
import uuid
from logging.handlers import RotatingFileHandler
from qcs_utils import cmd_utils

# 1Mbytes
def ERR_TRACE(level, string):

    # TRACE CTRL
    TRACE_ERROR = 0x0001
    TRACE_WARNING = 0x0002
    TRACE_ENTRY = 0x0004

    log_path='/var/log/qcs_iscsi_service.log'

    if not os.path.isfile(log_path):
        path = os.path.split(log_path)[0]
        try:
            os.makedirs(path)
        except:
            pass

    handler = RotatingFileHandler(log_path, mode='w', maxBytes = 1024*1024, backupCount = 1)
    formatter = logging.Formatter(fmt = '%(asctime)s %(name)-12s %(levelname)s %(message)s', datefmt = '[%Y/%m/%d %H:%M:%S]')
    handler.setFormatter(formatter)

    logger = logging.getLogger('qcs_iscsi_service')
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

class RBD_LIB():
    def __init__:
        # RBD cmd ctrl
        CMD_RBD = "/usr/local/ceph/bin/rbd"
        ID_KEYRING = " --id %s --keyring=/etc/ceph/ceph.client.%s.keyring"

        self.RBD_CREATE_IMAGE = CMD_RBD+" create --size %s --pool %s --image %s --image-feature layering"+ID_KEYRING
        self.RBD_CREATE_THICK_IMAGE = CMD_RBD+" create --size %s --pool %s --image %s --image-feature layering --thick-provision"+ID_KEYRING
        self.RBD_REMOVE_IMAGE = CMD_RBD+" remove --pool %s --image %s"+ID_KEYRING
        self.RBD_MAP_DEVICE = CMD_RBD+" map --pool %s --image %s"+ID_KEYRING
        self.RBD_UNMAP_DEVICE = CMD_RBD+" unmap --pool %s --image %s"+ID_KEYRING
        self.RBD_RESIZE_IMAGE = CMD_RBD+" resize --pool %s --image %s --size %s"
        self.RBD_RENAME_IMAGE = CMD_RBD+" rename --pool %s --image %s %s"
        self.RBD_GET_INFO = CMD_RBD+" info --pool %s --image %s --format json"+ID_KEYRING

    def qcs_check_image_exist(self, pool_name, lun_name):
        cmd = self.RBD_GET_INFO %(pool_name, lun_name, pool_name, pool_name) 
        ret = cmd_utils(cmd).check_output()
        return ret['return_code']

    def qcs_create_disk(self, disk_size, pool_name, lun_name):
        ret = self.qcs_check_image_exist(pool_name, lun_name)
        if ret is 0:
            dev = 0 # get dev with targetcli cmd
            ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_create_disk: disk existed, dev=%s"%(ret, dev))
        else:
            self._qcs_create_rbd_image(disk_size, pool_name, lun_name)
            ret, dev = self._qcs_map_rbd_to_device(pool_name, lun_name)
            if ret is not 0:
                return ret # FAIL qcs_create_disk

        index = self.qcs_parser_rbd_device_index(dev)
        stor_name = 'stor_lun'+index
        # targetcli create lun


    def _qcs_create_rbd_image(self, disk_size, pool_name, lun_name):
        cmd = self.RBD_CREATE_IMAGE %(disk_size, pool_name, lun_name, pool_name, pool_name)
        ret = cmd_utils(cmd).check_output()
        ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_create_rbd_image:%s"%(ret['return_code'], cmd))
        return ret['return_code']

    def _qcs_map_rbd_to_device(pool_name, lun_name):
        cmd = self.RBD_MAP_DEVICE %(pool_name, lun_name, pool_name, pool_name)
        ret = cmd_utils(cmd).check_output()
        ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_map_rbd_to_device:%s dev:%s"%(ret['return_code'], cmd, ret['json_output'][0]['raw_data']))
        return ret['return_code'], ret['json_output'][0]['raw_data']

    def qcs_parser_rbd_device_index(device):
        parse_name = '/dev/rbd'
        index = device[len(parse_name):]
        return index
        
    def qcs_remove_disk(self, pool_name, lun_name):
        ret = self.qcs_check_image_exist(pool_name, lun_name)
        if ret is 0:
            ret = self._qcs_unmap_rbd_from_device(pool_name, lun_name)
            if ret is 0:
                self._qcs_remove_rbd_image(pool, lun_name)
                ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_remove_disk: remove %s successfully."%(ret, lun_name))
            else:
                return ret #unmap fail
        else:
            ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_remove_disk: %s does not exist."%(ret, lun_name))
        return 0 #if lun does not exist, still return 0.

    def _qcs_unmap_rbd_from_device(self, pool_name, lun_name):
        cmd = self.RBD_UNMAP_DEVICE %(pool_name, lun_name, pool_name, pool_name) 
        ret = cmd_utils(cmd).check_output()
        ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_unmap_rbd_from_device:%s"%(ret['return_code'], cmd))
        if ret['return_code'] is not 0:
            ERR_TRACE(TRACE_ERROR, "_qcs_unmap_rbd_from_device: unmap %s fail."%(lun_name))
        return ret['return_code']

    def _qcs_remove_rbd_image(self, pool_name, lun_name):
        cmd = self.RBD_REMOVE_IMAGE %(pool_name, lun_name, pool_name, pool_name)
        ret = cmd_utils(cmd).check_output()
        ERR_TRACE(TRACE_ENTRY, "ret:%d _qcs_remove_rbd_image:%s"%(ret['return_code'], cmd))
        return ret['return_code']

class iSCSI_LIB():
    def __init__(self):
        CMD_TARGETCLI = "/usr/local/ceph/bin/targetcli"
    # targetcli cmd ctrl
        self.CREATE_TRGT = CMD_TARGETCLI+" /iscsi/ create %s"
        self.DELETE_TRGT = CMD_TARGETCLI+" /iscsi/ delete %s"
        self.ADD_TRGT_NP = CMD_TARGETCLI+" /iscsi/%s/tpg1/portals/ creat %s %s "
        self.TRGT_CTRL = CMD_TARGETCLI+" /iscsi/%s/tpg1 %s"
        self.TRGT_CHAP_CTRL = CMD_TARGETCLI+" /iscsi/%s/tpg1 set attribute authentication=%d"
        self.TRGT_CHAP_STATUS = CMD_TARGETCLI+" /iscsi/%s/tpg1 get attribute authentication"
        self.TRGT_SET_CRC = CMD_TARGETCLI+" /iscsi/%s/tpg1/ set parameter %s=%s"
        self.TRGT_SET_CHAP = CMD_TARGETCLI+" /iscsi/%s/tpg1 set auth %s=%s"
        self.TRGT_GET_CHAP = CMD_TARGETCLI+" /iscsi/%s/tpg1 get auth %s"
        self.TRGT_MAP_LUN = CMD_TARGETCLI+" /iscsi/%s/tpg1/luns create storage_object=%s lun=%s false"
        self.TRGT_UNMAP_LUN = CMD_TARGETCLI+" /iscsi/%s/tpg1/luns delete lun=%s"
        self.ADD_INIT = CMD_TARGETCLI+" /iscsi/%s/tpg1/acls create %s"
        self.REMOVE_INIT = CMD_TARGETCLI+" /iscsi/%s/tpg1/acls delete %s"
        self.INIT_SET_CHAP = CMD_TARGETCLI+" /iscsi/%s/tpg1/acls/%s set auth %s=%s"
        self.INIT_LINK_LUN = CMD_TARGETCLI+" /iscsi/%s/tpg1/acls/%s create mapped_lun=%s tpg_lun_or_backstore=lun%s write_protect=%s"
        self.INIT_UNLINK_LUN = CMD_TARGETCLI+" /iscsi/%s/tpg1/acls/%s delete mapped_lun=%s"
    # targetcli IQN ctrl
        self.DEFAULT_INIT = "iqn.2004-04.com.qnap:all:iscsi.default.ffffff"
        self.TRGT_PREFIX = "iqn.2004-04.com.qnap:qcs-vm:iscsi.%s.vat80682695"
        self.TRGT_LIO = "/sys/kernel/config/target/iscsi/%s/tpgt_1/acls/"
    
def qcs_get_vm_host_ip():
    import socket
    hostname = socket.gethostname()
    path = "/share/CACHEDEV1_DATA/.config/etc/nodes/%s/.qsgw.conf"%(hostname)
    ip = INI_CONF(path).Ini_Conf_Get_Field(hostname, "IP")
    return ip

def qcs_check_initiator(trgt_iqn, init_iqn):
    if os.path.isdir((TRGT_LIO+"%s")%(trgt_iqn, init_iqn)):
        return DEVICE_EXISTED
    return 0 # NOT EXISTED

def qcs_check_target_is_empty_acls(trgt_iqn):
    if os.listdir(TRGT_LIO%(trgt_iqn)):
        return DEVICE_EXISTED
    return 0 # EMPTY

def qcs_get_trgt_iqn(trgt_name):
    trgt_iqn = TRGT_PREFIX%(trgt_name)
    return trgt_iqn

def qcs_create_target(trgt_iqn):
    cmd = CREATE_TRGT%(trgt_iqn)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_create_target:%s"%(ret['return_code'], cmd))
    # add network portal
    ip = qcs_get_vm_host_ip()
    cmd = ADD_TRGT_NP%(trgt_iqn, ip, "3260")
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_create_target:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_target_ctrl(trgt_iqn, enable):
    cmd = TRGT_CTRL%(trgt_iqn, "enable") if enable else TRGT_CTRL%(trgt_iqn, "disable")
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_target_ctrl:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_trgt_set_crc(trgt_iqn, crc_opts):
    # Set DataDigest
    if crc_opts['data_digest'] is 1:
        cmd = TRGT_SET_CRC%(trgt_iqn, "DataDigest", "CRC32C")
    else:
        cmd = TRGT_SET_CRC%(trgt_iqn, "DataDigest", "CRC32C,None")
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_crc:%s"%(ret['return_code'], cmd))
    # Set HeaderDigest
    if crc_opts['header_digest'] is 1:
        cmd = TRGT_SET_CRC%(trgt_iqn, "HeaderDigest", "CRC32C")
    else:
        cmd = TRGT_SET_CRC%(trgt_iqn, "HeaderDigest", "CRC32C,None")
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_crc:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_trgt_set_chap(trgt_iqn, chap_opts):
    enable = 0
    if chap_opts['enable'] or chap_opts['mutual_enable'] == 1: #at least 1 enable
        enable = 1
    # enable auth
    cmd = TRGT_CHAP_CTRL%(trgt_iqn, enable)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_chap:%s"%(ret['return_code'], cmd))
    # set userid
    cmd = TRGT_SET_CHAP%(trgt_iqn, "userid", chap_opts['userid']) 
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_chap:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    # set password
    cmd = TRGT_SET_CHAP%(trgt_iqn, "password", chap_opts['password']) 
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_chap:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    # set mutual_userid
    cmd = TRGT_SET_CHAP%(trgt_iqn, "mutual_userid", chap_opts['mutual_userid']) 
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_chap:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    # set mutual_password
    cmd = TRGT_SET_CHAP%(trgt_iqn, "mutual_password", chap_opts['mutual_password']) 
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_trgt_set_chap:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    return ret['return_code']

def qcs_map_lun_to_trgt(trgt_iqn, lun_name):
    cmd = TRGT_MAP_LUN%(trgt_iqn, lun_name['stor_object'], lun_name['index'])
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_map_lun_to_trgt:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    return ret['return_code']

def qcs_unmap_lun_from_trgt(trgt_iqn, lun_name):
    cmd = TRGT_UNMAP_LUN%(trgt_iqn, lun_name['index'])
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_unmap_lun_from_trgt:%s"%(ret['return_code'], cmd))
    ret = cmd_utils(cmd).check_output()
    return ret['return_code']

def qcs_delete_target(trgt_name):
    cmd = DELETE_TRGT%(trgt_iqn)
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_delete_target:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_add_init(trgt_iqn, init_iqn):
    cmd = ADD_INIT%(trgt_iqn, init_iqn)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_add_init:%s"%(ret['return_code'], cmd))
    # After adding init, must check chap and chap_mutual
    enable, chap = get_target_chap(trgt_iqn)
    if enable:
        # set userid
        cmd = INIT_SET_CHAP%(trgt_iqn, init_iqn, "userid", chap['userid'])
        ret = cmd_utils(cmd).check_output()
        # set password
        cmd = INIT_SET_CHAP%(trgt_iqn, init_iqn, "password", chap['password'])
        ret = cmd_utils(cmd).check_output()
        # set mutual_userid
        cmd = INIT_SET_CHAP%(trgt_iqn, init_iqn, "mutual_userid", chap['mutual_userid'])
        ret = cmd_utils(cmd).check_output()
        # set mutual_password
        cmd = INIT_SET_CHAP%(trgt_iqn, init_iqn, "mutual_password", chap['mutual_password'])
        ret = cmd_utils(cmd).check_output()
    # disable do nothing
    ERR_TRACE(TRACE_ENTRY, "qcs_add_init:chap enable=%d"%(enable))
    return ret['return_code']

def qcs_init_link_lun(trgt_iqn, init_iqn, lun_name, access):
    if access is not -1:
        cmd = INIT_LINK_LUN%(trgt_iqn, init_iqn, file_data[lun]['index'], file_data[lun]['index'], access)
        ret = cmd_utils(cmd).check_output()
        ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_init_link_lun:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_init_unlink_lun(trgt_iqn, init_iqn, lun_name):
    cmd = INIT_UNLINK_LUN%(trgt_iqn, init_iqn, lun_name['index'])
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_init_unlink_lun:%s"%(ret['return_code'], cmd))
    return ret['return_code']

def qcs_init_modify_lun_access(trgt_iqn, init_iqn, luns, access):
    ret = qcs_init_unlink_lun(trgt_iqn, init_iqn, luns)
    if ret is 0:
        ret = qcs_init_link_lun(trgt_iqn, init_iqn, luns, access)
    ERR_TRACE(TRACE_ENTRY, "qcs_init_modify_lun_access: ret=%d"%(ret))
    return ret

def get_target_chap(trgt_iqn):
    cmd = TRGT_CHAP_STATUS%(trgt_iqn)
    ret = cmd_utils(cmd).check_output()
    enable = 1 if ret['json_output'][0]['raw_data'].split('=')[1] is '1' else 0
    dic = {}
    if enable: #get auth value
        # get userid
        cmd = TRGT_GET_CHAP%(trgt_iqn, "userid")
        ret = cmd_utils(cmd).check_output()
        userid = ret['json_output'][0]['raw_data'].split('=')[1]
        # get password
        cmd = TRGT_GET_CHAP%(trgt_iqn, "password")
        ret = cmd_utils(cmd).check_output()
        password = ret['json_output'][0]['raw_data'].split('=')[1]
        # get mutual_userid
        cmd = TRGT_GET_CHAP%(trgt_iqn, "mutual_userid")
        ret = cmd_utils(cmd).check_output()
        mutual_userid = ret['json_output'][0]['raw_data'].split('=')[1]
        # get mutual_password
        cmd = TRGT_GET_CHAP%(trgt_iqn, "mutual_password")
        ret = cmd_utils(cmd).check_output()
        mutual_password = ret['json_output'][0]['raw_data'].split('=')[1]
        dic = {'userid': userid, 'password': password, 'mutual_userid': mutual_userid, 'mutual_password': mutual_password}
    return enable, dic

def qcs_remove_init(trgt_iqn, init_iqn):
    cmd = REMOVE_INIT%(trgt_iqn, init_iqn)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_remove_init:%s"%(ret['return_code'], cmd))
    return ret['return_code']
# QCS VM CTRL - END

# QCS HOST CTRL - Start
# HOST and VM use same config, but different path
def qcs_get_lun_list(pool):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    data = qcs_get_disk_data(HOST_LUN_CONFIG)
    ret = []
    for key in data:
        if key != 'Global' and key != 'acl_trgts' and key != 'acl_luns':
            ret.append(key)
    ERR_TRACE(TRACE_ENTRY, "qcs_get_lun_list: %s"%(ret))
    if ret == []:
        ERR_TRACE(TRACE_ERROR, "qcs_get_lun_list: none lun existed")
        return -1
    return ret

def qcs_resize_lun(pool, lun_name, disk_size):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    data = qcs_get_disk_data(HOST_LUN_CONFIG)
    image_name = data[lun_name]['image_name']
    cmd = RBD_RESIZE_IMAGE %(pool, image_name, disk_size)
    ret = cmd_utils(cmd).check_output()
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_resize_lun:%s"%(ret['return_code'], cmd))
    if ret['return_code'] is 0:
        ERR_TRACE(TRACE_ENTRY, "qcs_resize_lun:%s resize %s to %s "%(lun_name, data[lun_name]['size'], disk_size))
        data[lun_name]['size'] = disk_size
        ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(data)
    return ret

def qcs_rename_image(pool, old_name, new_name):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    data = qcs_get_disk_data(HOST_LUN_CONFIG)
    data[new_name] = data.pop(old_name)# update key name
    data[new_name]['lusn_name'] = new_name
    ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(data)
    ERR_TRACE(TRACE_ENTRY, "ret:%d qcs_rename_image: rename %s to %s"%(ret, old_name, new_name))
    return ret

def qcs_create_lun_acl_config(pool, data):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    file_data = qcs_get_disk_data(HOST_LUN_CONFIG)
    file_data['acl_luns'].update(data)
    ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(file_data)
    return ret

def qcs_create_trgt_acl_config(pool, data):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    file_data = qcs_get_disk_data(HOST_LUN_CONFIG)
    file_data['acl_trgts'].update(data)
    ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(file_data)
    return ret

def qcs_delete_lun_acl_config(pool, init_iqn):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    file_data = qcs_get_disk_data(HOST_LUN_CONFIG)
    del file_data['acl_luns'][init_iqn]
    ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(file_data)
    return ret

def qcs_delete_trgt_acl_config(pool, trgt_iqn):
    HOST_LUN_CONFIG = qcs_get_host_lun_conf(pool)
    file_data = qcs_get_disk_data(HOST_LUN_CONFIG)
    del file_data['acl_trgts'][trgt_iqn]
    ret = JSON_CONF(HOST_LUN_CONFIG).JSON_Write_Conf(file_data)
    return ret

def qcs_get_host_lun_conf(pool):
    cepf_root = qcs_get_ceph_root()
    config_path = cepf_root+'/QSGW/'+pool+'/.config/iscsi/qcs_iscsi_lun.json'
    return config_path

def qcs_get_ceph_root():
    cmd = "mount | grep CEPH | grep -Ev bind | awk '{print $3}'"
    ret = cmd_utils(cmd).check_output()
    return ret['json_output'][0]['raw_data']

# Others
def qcs_parser_rbd_device_index(device):
    parse_name = '/dev/rbd'
    index = device[len(parse_name):]
    return index

def qcs_check_lun_exist(lun_name, config_file):
    data = JSON_CONF(config_file).JSON_Read_Conf()
    try:
        data[lun_name]
        return DEVICE_EXISTED
    except:
        return 0

def qcs_get_disk_data(config_file):
    data = JSON_CONF(config_file).JSON_Read_Conf()
    return data

# targetcli CTRL
def parser_check_output(return_message):
    return_message = return_message.replace(' ','')
    split_string = return_message.split(',')
    dic = {}
    for i in range(len(split_string)):
        data = split_string[i].split(':')
        dic[data[0]] = data[1]
    return dic
