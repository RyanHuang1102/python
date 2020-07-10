mesg_code_table = {
    # LUN ACL
    'CREATE_LUN_ACL_SUCCESS':
    {'mesg':'[{0}] VM {1} Created LUN ACL policy {2} for initiator {3}.',
     'level':'NORMAL'
    },
    'CREATE_LUN_ACL_FAIL':
    {'mesg':'[{0}] VM {1} Fail to create LUN ACL policy {2} for initiator {3}.',
     'level':'CRITICAL'
    },
    'REMOVE_LUN_ACL_SUCCESS':
    {'mesg':'[{0}] VM {1} Removed LUN ACL policy for initiator {2}.',
     'level':'NORMAL'
    },
    'REMOVE_LUN_ACL_FAIL':
    {'mesg':'[{0}] VM {1} Failed to remove LUN ACL policy for initiator {2}.',
     'level':'CRITICAL'
    },
    'UPDATE_LUN_ACL_POLICY_NAME_SUCCESS':
    {'mesg':'[{0}] VM {1} Changed LUN ACL policy name for initiator {2}. New policy name: {3}.',
     'level':'NORMAL'
    },
    'UPDATE_LUN_ACL_POLICY_NAME_FAIL':
    {'mesg':'[{0}] VM {1} Failed to change LUN ACL policy name for initiator {2}.',
     'level':'CRITICAL'
    },
    'UPDATE_LUN_ACL_POLICY_SUCCESS':
    {'mesg':'[{0}] VM {1} Modified LUN ACL. LUN: {2}, New permissions: {3}.',
     'level':'NORMAL'
    },
    'UPDATE_LUN_ACL_POLICY_FAIL':
    {'mesg':'[{0}] VM {1} Fail to modified LUN ACL. LUN: {2}, New permissions: {3}.',
     'level':'CRITICAL'
    },
    # LUN
    'START_CREATING_THIN_LUN':
    {'mesg':'[{0}] VM {1} Started allocating space to LUN {2}. LUN capacity: {3}GB, Provisioning: Thin.',
     'level':'NORMAL'
    },
    'START_CREATING_THICK_LUN':
    {'mesg':'[{0}] VM {1} Started allocating space to LUN {2}. LUN capacity: {3}GB, Provisioning: Thick.',
     'level':'NORMAL'
    },
    'CREATE_LUN_SUCCESS':
    {'mesg':'[{0}] VM {1} Finished allocating space to LUN {2}. LUN capacity: {3}GB',
     'level':'NORMAL'   
    },
    'CREATE_LUN_FAIL':
    {'mesg':'[{0}] VM {1} Failed to create LUN {2}. LUN capacity: {3}GB.',
     'level':'CRITICAL'
    },
    'CREATE_LUN_FAIL_NO_SPACE_LEFT':
    {'mesg':'[{0}] VM {1} Failed to create LUN {2}. LUN capacity: {3}GB, Insufficient storage space.',
     'level':'CRITICAL'
    },
    'UPDATE_LUN_SPACE_SUCCESS':
    {'mesg':'[{0}] VM {1} Finished expanding LUN {2}. New capacity: {3}GB.',
    'level':'CRITICAL'
    },
    'DELETE_LUN_SUCCESS':
    {'mesg':'[{0}] VM {1} Deleted LUN {2}',
     'level':'NORMAL'
    },
    'DELETE_LUN_FAIL':
    {'mesg':'[{0}] VM {1} Failed to delete LUN {2}',
     'level':'CRITICAL'
    },
    # TARGET 
    'CREATE_TARGET_SUCCESS':
    {'mesg':'[{0}] VM {1} Created iSCSI target {2}',
     'level':'NORMAL'
    },
    'CREATE_TARGET_FAIL':
    {'mesg':'[{0}] VM {1} Failed to create iSCSI target {2}',
     'level':'CRITICAL'
    },
    'ENABLE_TARGET':
    {'mesg':'[{0}] VM {1} Enabled iSCSI target {2}',
     'level':'NORMAL'
    },
    'DISABLE_TARGET':
    {'mesg':'[{0}] VM {1} Disabled iSCSI target {2}',
     'level':'NORMAL'
    },
    'ENABLE_TARGET_AUTH':
    {'mesg':'[{0}] VM {1} Enabled iSCSI target {2} authentication.',
     'level':'NORMAL'
    },
    'DISABLE_TARGET_AUTH':
    {'mesg':'[{0}] VM {1} Disabled iSCSI target {2} authentication.',
     'level':'NORMAL'
    },
    'SET_TARGET_ALLOW_ALL':
    {'mesg':'[{0}] VM {1} Allowed iSCSI target {2} can be connected by all initiators.',
     'level':'NORMAL'
    },
    'SET_TARGET_ALLOW_FROM_LIST':
    {'mesg':'[{0}] VM {1} Allowed iSCSI target {2} can be connected by initiators only from the ACL list.',
     'level':'NORMAL'
    },
    'REMOVE_TARGET_SUCCESS':
    {'mesg':'[{0}] VM {1} Removed iSCSI target {2}.',
     'level':'NORMAL'
    },
    'REMOVE_TARGET_FAIL':
    {'mesg':'[{0}] VM {1} Failed to remove iSCSI target {2}.',
     'level':'CRITICAL'
    },
    'MAP_LUN_TO_TARGET_SUCCESS':
    {'mesg':'[{0}] VM {1} Mapped LUN {2} to iSCSI target {3}.',
     'level':'NORMAL'
    },
    'MAP_LUN_TO_TARGET_FAIL':
    {'mesg':'[{0}] VM {1} Fail to map LUN {2} to iSCSI target {3}.',
     'level':'CRITICAL'
    },
    'UNMAP_LUN_FROM_TARGET_SUCCESS':
    {'mesg':'[{0}] VM {1} Unmapped LUN {2} from iSCSI target {3}.',
     'level':'NORMAL'
    },
    'UNMAP_LUN_FROM_TARGET_FAIL':
    {'mesg':'[{0}] VM {1} Fail to unmap LUN {2} from iSCSI target {3}.',
     'level':'CRITICAL'
    }
}
