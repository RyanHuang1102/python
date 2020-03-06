#!/usr/bin/python

from lib import *
from err_trace import *
log_path = 'iscsi.log'
config_path = 'test.cfg'

Config = config(config_path)

ret = Config.Ini_Conf_Set_Field('mylun', 'dev', '/dev/rbd')

print ret

