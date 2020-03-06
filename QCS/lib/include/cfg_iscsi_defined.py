TARGET_FILE = "iscsi_trgt.cfg"
INITIATOR_FILE = "iscsi_init.cfg"
LUN_FILE = "iscsi_lun.cfg"

MAX_IDX_BMP_SIZE = 32
MAX_ISCSI_TARGET = 256
MAX_ISCSI_INITIATOR = 256
MAX_ISCSI_LUN = 256

#ERROR CONTROL
GET_LOCK_FILE_FAIL = -2

#BITMAP CONTROL
CFG_GLOBAL = "Global"
CFG_TARGET_BITMAP = "targetBitmap"
CFG_INITIATOR_BITMAP = "initiatorBitmap"
CFG_LUN_BITMAP = "LUNBitmap"

#TARGET CONTROL
targetIQNPrefix = "iqn.2004-04.com.qnap:qcs:iscsi."
CFG_TARGET_KEY_SEC = "TargetKey"
CFG_TARGET_INFOK = "target_"
CFG_TARGET_INFOI = "target%dInfo"
CFG_TARGET_INDEX = "targetIndex"
CFG_TARGET_NAME = "targetName"
CFG_TARGET_IQN = "targetIQN"
CFG_TARGET_ALIAS = "targetAlias"
CFG_TARGET_STATUS = "targetStatus"
#target status
TARGET_OFFLINE = -1
TARGET_READY = 0
TARGET_CONNECTED = 1

#FILE LOCK CONTROL
MAX_TRY = 20
