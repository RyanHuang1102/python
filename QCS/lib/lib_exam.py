#!/usr/bin/python

from lib import *
from log import *
log_path = 'my.log'
config_path = 'test.cfg'

Config = config(config_path)

ret = Config.Ini_Conf_Set_Field('mylun', 'dev', '/dev/rbd')

log = LOG(log_path ,config_path)
log.INFO_TRACE(TRACE_ERROR,"Config.Ini_Conf_Set_Field('mylun', 'dev', '/dev/rbd') ret:%d" %ret)



